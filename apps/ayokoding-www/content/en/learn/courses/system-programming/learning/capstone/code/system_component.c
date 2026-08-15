/* Pooled TCP Frame Exchange.
 * Demonstrates: one pool-slot owner, big-endian wire bytes, and POSIX socket
 * cleanup. Compile with -std=c11 -Wall -Wextra -Werror. */
#define _POSIX_C_SOURCE 200112L

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

enum { POOL_CAPACITY = 4, WIRE_BYTES = 4 };

struct frame {
  uint32_t value;
  int in_use;
};

struct pool {
  struct frame slots[POOL_CAPACITY];
};

static struct frame *pool_acquire(struct pool *pool) {
  for (size_t i = 0; i < POOL_CAPACITY; ++i) {
    if (!pool->slots[i].in_use) {
      pool->slots[i].in_use = 1; /* pool transfers this slot to caller */
      return &pool->slots[i];
    }
  }
  return NULL;
}

static void pool_release(struct frame *frame) {
  if (frame != NULL) {
    frame->value = 0;
    frame->in_use =
        0; /* release exactly once by clearing its ownership state */
  }
}

static void encode_u32(uint32_t value, unsigned char out[WIRE_BYTES]) {
  uint32_t network = htonl(value);
  memcpy(out, &network, WIRE_BYTES); /* byte copy, never struct-as-wire */
}

static uint32_t decode_u32(const unsigned char in[WIRE_BYTES]) {
  uint32_t network;
  memcpy(&network, in, WIRE_BYTES);
  return ntohl(network);
}

static int write_all(int fd, const unsigned char *buffer, size_t length) {
  while (length > 0) {
    ssize_t written = send(fd, buffer, length, 0);
    if (written <= 0)
      return -1;
    buffer += (size_t)written;
    length -= (size_t)written;
  }
  return 0;
}

static int read_all(int fd, unsigned char *buffer, size_t length) {
  while (length > 0) {
    ssize_t received = recv(fd, buffer, length, 0);
    if (received <= 0)
      return -1;
    buffer += (size_t)received;
    length -= (size_t)received;
  }
  return 0;
}

static int client(uint16_t port, uint32_t sent) {
  int fd = -1, result = 1;
  struct sockaddr_in address;
  unsigned char wire[WIRE_BYTES];

  fd = socket(AF_INET, SOCK_STREAM, 0);
  if (fd < 0)
    goto cleanup;
  memset(&address, 0, sizeof address);
  address.sin_family = AF_INET;
  address.sin_port = htons(port);
  if (inet_pton(AF_INET, "127.0.0.1", &address.sin_addr) != 1)
    goto cleanup;
  if (connect(fd, (const struct sockaddr *)&address, sizeof address) != 0)
    goto cleanup;
  encode_u32(sent, wire);
  if (write_all(fd, wire, sizeof wire) != 0 ||
      read_all(fd, wire, sizeof wire) != 0)
    goto cleanup;
  if (decode_u32(wire) != sent)
    goto cleanup;
  result = 0;

cleanup:
  if (result != 0 && errno != 0)
    perror("client");
  if (fd >= 0)
    close(fd);
  return result;
}

int main(void) {
  const uint32_t expected = UINT32_C(0x10203040);
  int listen_fd = -1, peer_fd = -1, result = 1, child_status = 0, reuse = 1;
  pid_t child = -1;
  struct sockaddr_in address;
  socklen_t address_length = sizeof address;
  struct pool pool = {0};
  struct frame *frame = NULL;
  unsigned char wire[WIRE_BYTES];

  listen_fd = socket(AF_INET, SOCK_STREAM, 0);
  if (listen_fd < 0)
    goto cleanup;
  if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof reuse) !=
      0)
    goto cleanup;
  memset(&address, 0, sizeof address);
  address.sin_family = AF_INET;
  if (inet_pton(AF_INET, "127.0.0.1", &address.sin_addr) != 1)
    goto cleanup;
  address.sin_port = 0; /* kernel selects a local test port */
  if (bind(listen_fd, (const struct sockaddr *)&address, sizeof address) != 0)
    goto cleanup;
  if (listen(listen_fd, 1) != 0)
    goto cleanup;
  if (getsockname(listen_fd, (struct sockaddr *)&address, &address_length) != 0)
    goto cleanup;
  child = fork();
  if (child < 0)
    goto cleanup;
  if (child == 0)
    _exit(client(ntohs(address.sin_port), expected));

  peer_fd = accept(listen_fd, NULL, NULL);
  if (peer_fd < 0) {
    perror("accept");
    goto cleanup;
  }
  frame = pool_acquire(&pool);
  if (frame == NULL) {
    fputs("pool empty\n", stderr);
    goto cleanup;
  }
  if (read_all(peer_fd, wire, sizeof wire) != 0) {
    perror("read");
    goto cleanup;
  }
  frame->value = decode_u32(wire);
  if (frame->value != expected) {
    fputs("wrong frame\n", stderr);
    goto cleanup;
  }
  encode_u32(frame->value, wire);
  if (write_all(peer_fd, wire, sizeof wire) != 0) {
    perror("write");
    goto cleanup;
  }
  result = 0;

cleanup:
  pool_release(frame);
  if (peer_fd >= 0)
    close(peer_fd);
  if (listen_fd >= 0)
    close(listen_fd);
  if (child > 0 && (waitpid(child, &child_status, 0) < 0 ||
                    !WIFEXITED(child_status) || WEXITSTATUS(child_status) != 0))
    result = 1;
  if (result == 0)
    puts("PASS: pool ownership, big-endian echo, and socket cleanup");
  else if (errno != 0)
    perror("system_component");
  return result;
}

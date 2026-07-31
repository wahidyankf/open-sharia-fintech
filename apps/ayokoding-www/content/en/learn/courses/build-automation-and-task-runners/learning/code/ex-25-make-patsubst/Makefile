# Transform each discovered source filename into an object filename.
SRCS := $(wildcard *.c)
OBJS := $(patsubst %.c,%.o,$(SRCS))

.PHONY: show
show:
	@printf '%s\n' "$(OBJS)"

// Fine-grained signals capstone runtime: reads subscribe the active effect.
export type Signal<T> = { get value(): T; set value(value: T) };
type Effect = () => void;
let active: Effect | undefined;

export function signal<T>(initial: T): Signal<T> {
  let value = initial;
  const subscribers = new Set<Effect>();
  return {
    get value(): T {
      if (active) subscribers.add(active);
      return value;
    },
    set value(next: T) {
      if (Object.is(value, next)) return;
      value = next;
      subscribers.forEach((subscriber) => subscriber());
    },
  };
}

export function effect(run: Effect): () => void {
  const wrapped = (): void => {
    active = wrapped;
    run();
    active = undefined;
  };
  wrapped();
  return (): void => undefined;
}

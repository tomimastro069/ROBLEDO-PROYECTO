import { useState, useTransition, useCallback } from 'react';

export function useActionState<State, Payload>(
  action: (state: State, payload: Payload) => State | Promise<State>,
  initialState: State
): [State, (payload: Payload) => void, boolean] {
  const [state, setState] = useState<State>(initialState);
  const [isPending, startTransition] = useTransition();

  const dispatch = useCallback(
    (payload: Payload) => {
      startTransition(() => {
        const result = action(state, payload);
        if (result instanceof Promise) {
          result.then(setState);
        } else {
          setState(result);
        }
      });
    },
    [action, state]
  );

  return [state, dispatch, isPending];
}

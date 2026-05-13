export type FormState<T> = {
  isSuccess: boolean;
  message?: string;
  errors?: Partial<Record<keyof T, string>>;
};

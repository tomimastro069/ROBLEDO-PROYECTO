export function handleError(error: unknown, context: string): string {
  console.error(`[Error] ${context}:`, error);
  if (error instanceof Error) return error.message;
  return String(error);
}

export function logWarning(message: string, context: string) {
  console.warn(`[Warn] ${context}:`, message);
}

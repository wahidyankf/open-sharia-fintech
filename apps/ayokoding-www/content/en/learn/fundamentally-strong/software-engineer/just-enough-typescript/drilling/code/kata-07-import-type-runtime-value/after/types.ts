// Kata 7: types.ts -- ApiError is a class, so it exists as BOTH a type and a runtime value.
export class ApiError extends Error {
  constructor(
    public readonly statusCode: number,
    message: string,
  ) {
    super(message);
  }
}

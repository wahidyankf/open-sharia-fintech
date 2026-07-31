export const handler = async (event) => ({
  statusCode: 200,
  body: JSON.stringify({ receivedRecords: event.Records?.length ?? 0 }),
});

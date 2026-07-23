// Example 53: Intersection Config Merge -- combine two option shapes into one required shape.
type WithRetry = { retries: number };
type WithTimeout = { timeoutMs: number };
type RequestOptions = WithRetry & WithTimeout; // => needs BOTH retries and timeoutMs

const options: RequestOptions = { retries: 3, timeoutMs: 5000 }; // => both member sets required
console.log(options); // => Output: { retries: 3, timeoutMs: 5000 }

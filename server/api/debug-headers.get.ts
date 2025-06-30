export default defineEventHandler(async (event) => {
  const headers = getRequestHeaders(event);
  const requestURL = getRequestURL(event);

  const debugInfo = {
    nodeEnv: process.env.NODE_ENV,
    headers: {
      origin: headers.origin,
      host: headers.host,
      "x-forwarded-proto": headers["x-forwarded-proto"],
      referer: headers.referer,
    },
    requestURL: {
      href: requestURL.href,
      origin: requestURL.origin,
      protocol: requestURL.protocol,
      host: requestURL.host,
      hostname: requestURL.hostname,
      port: requestURL.port,
    },
    constructedOrigin: {
      fromRequestURL: requestURL.origin,
      fromHeaders:
        headers.origin ||
        `${headers["x-forwarded-proto"] || "http"}://${headers.host}`,
      isLocalDev: process.env.NODE_ENV === "development",
      finalOrigin:
        process.env.NODE_ENV === "development"
          ? "http://localhost:3000"
          : requestURL.origin !== "null"
          ? requestURL.origin
          : headers.origin ||
            `${headers["x-forwarded-proto"] || "http"}://${headers.host}`,
    },
  };

  console.error("Debug endpoint called:", debugInfo);

  return debugInfo;
});

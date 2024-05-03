export const baseUrl = "http://localhost:5001";

export const postRequest = async (url, body, customHeaders = {}) => {
  const headers = {
    "Content-Type": "application/json",
    ...customHeaders,
  };
  const response = await fetch(url, {
    method: "POST",
    headers: headers,
    body,
  });

  const data = await response.json();
  if (!response.ok) {
    let message;
    if (data?.message) {
      message = data.message;
    } else {
      message = data;
    }
    return { error: true, message };
  }

  return data;
};

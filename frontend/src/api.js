import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "https://pdf-chatbot-api-9zrk.onrender.com";

export async function uploadPDF(file) {
  const formData = new FormData();
  formData.append("file", file);

  // Let axios set Content-Type with boundary; don't set it manually or the upload can fail
  const response = await axios.post(`${API_URL}/upload-pdf/`, formData);

  return response.data;
}

export async function queryPDF(question) {
  const response = await axios.post(
    `${API_URL}/query/`,
    { question },
    { headers: { "Content-Type": "application/json" } }
  );

  return response.data;
}

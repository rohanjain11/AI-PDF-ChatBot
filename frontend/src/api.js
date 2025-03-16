const API_URL = "http://127.0.0.1:8000";

export async function uploadPDF(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/upload-pdf/`, {
        method: "POST",
        body: formData
    });

    return response.json();
}

export async function queryPDF(question) {
    const response = await fetch(`${API_URL}/query/?question=${encodeURIComponent(question)}`, {
        method: "POST"
    });

    return response.json();
}

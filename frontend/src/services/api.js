import axios from 'axios';

const API_BASE_URL = "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor for the Authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("casepulse_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const loginUser = async (credentials) => {
  try {
    const response = await api.post('/auth/login', credentials);
    if (response.data.access_token) {
      localStorage.setItem("casepulse_token", response.data.access_token);
      localStorage.setItem("casepulse_user", JSON.stringify(response.data.user));
    }
    return response.data;
  } catch (error) {
    console.error("Login failed:", error);
    throw error;
  }
};

export const signupUser = async (userData) => {
  try {
    const response = await api.post('/auth/signup', userData);
    return response.data;
  } catch (error) {
    console.error("Signup failed:", error);
    throw error;
  }
};

export const logoutUser = () => {
  localStorage.removeItem("casepulse_token");
  localStorage.removeItem("casepulse_user");
};

export const getCurrentUser = () => {
  const user = localStorage.getItem("casepulse_user");
  return user ? JSON.parse(user) : null;
};

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading PDF:", error);
    throw error;
  }
};

export const extractCase = async (caseId) => {
  try {
    const response = await api.get(`/extract/${caseId}`);
    return response.data;
  } catch (error) {
    console.error("Error extracting case:", error);
    throw error;
  }
};

export const generateActionPlan = async (caseId) => {
  try {
    const response = await api.post(`/action-plan/${caseId}`);
    return response.data;
  } catch (error) {
    console.error("Error generating action plan:", error);
    throw error;
  }
};

export const getReview = async (caseId) => {
  try {
    const response = await api.get(`/review/${caseId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching review:", error);
    throw error;
  }
};

export const verifyCase = async (caseId, data) => {
  try {
    const response = await api.post(`/verify/${caseId}`, data);
    return response.data;
  } catch (error) {
    console.error("Error verifying case:", error);
    throw error;
  }
};

export const getDashboardSummary = async () => {
  try {
    const response = await api.get('/dashboard/summary');
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard summary:", error);
    throw error;
  }
};

export const getDashboardActions = async () => {
  try {
    const response = await api.get('/dashboard/actions');
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard actions:", error);
    throw error;
  }
};

export const getCaseDetails = async (caseId) => {
  try {
    const response = await api.get(`/cases/${caseId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching case details:", error);
    throw error;
  }
};

export const getAudit = async (caseId) => {
  try {
    const response = await api.get(`/audit/${caseId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching audit logs:", error);
    throw error;
  }
};

export const getMLPipeline = async (caseId) => {
  try {
    const response = await api.get(`/ml/pipeline/${caseId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching ML pipeline:", error);
    throw error;
  }
};

export const translateText = async (text, targetLanguage) => {
  try {
    const response = await api.post("/translate", {
      text,
      target_language: targetLanguage,
    });
    return response.data.translated_text;
  } catch (error) {
    console.error("Error translating text:", error);
    throw error;
  }
};

export const generateCaseSummary = async (caseId) => {
  const response = await api.post(`/case-summary/generate/${caseId}`);
  return response.data;
};

export const getCaseSummary = async (caseUid) => {
  const response = await api.get(`/case-summary/${caseUid}`);
  return response.data;
};

export const searchCaseByUid = async (caseUid) => {
  const response = await api.get(`/search/case/${caseUid}`);
  return response.data;
};

export const getPublicCase = async (caseUid) => {
  const response = await api.get(`/public/case/${caseUid}`);
  return response.data;
};

export const getQrData = async (caseUid) => {
  const response = await api.get(`/case-summary/qr/${caseUid}`);
  return response.data;
};

export const analyzeLegalSection = async (query) => {
  const response = await api.post(`/legal-sections/analyze`, { query });
  return response.data;
};

export default {
  uploadPDF,
  extractCase,
  generateActionPlan,
  getReview,
  verifyCase,
  getDashboardSummary,
  getDashboardActions,
  getCaseDetails,
  getAudit,
  getMLPipeline,
  translateText,
  loginUser,
  signupUser,
  logoutUser,
  getCurrentUser,
  generateCaseSummary,
  getCaseSummary,
  searchCaseByUid,
  getPublicCase,
  getQrData,
  analyzeLegalSection,
};

// Backend API calls

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:3001/api";

/**
 * Upload a PDF file to the backend
 * @param {File} file - The PDF file to upload
 * @returns {Promise} Response from backend
 */
export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: "POST",
      body: formData,
    });
    return await response.json();
  } catch (error) {
    console.error("Error uploading PDF:", error);
    throw error;
  }
};

/**
 * Get extracted data for a case
 * @param {string} caseId - The case ID
 * @returns {Promise} Extracted data from backend
 */
export const getExtractedData = async (caseId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/cases/${caseId}/data`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching extracted data:", error);
    throw error;
  }
};

/**
 * Get action plan for a case
 * @param {string} caseId - The case ID
 * @returns {Promise} Action plan from backend
 */
export const getActionPlan = async (caseId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/cases/${caseId}/action-plan`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching action plan:", error);
    throw error;
  }
};

/**
 * Get dashboard statistics
 * @returns {Promise} Dashboard stats from backend
 */
export const getDashboardStats = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/stats`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching dashboard stats:", error);
    throw error;
  }
};

export default {
  uploadPDF,
  getExtractedData,
  getActionPlan,
  getDashboardStats,
};

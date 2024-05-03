import axios from "axios";

export const loginUser = async (email, password) => {
  try {
    const response = await axios.post("http://localhost:5000/api/auth/login", {
      email,
      password,
    });

    if (response.status === 200) {
      return response.data;
    }

    if (response.data.errors) {
      console.error("Errors from server:", response.data.errors);
      throw new Error("Server returned errors");
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const responseData = error.response.data;
      throw new Error(responseData.message || "An error occurred");
    } else {
      throw error;
    }
  }
};

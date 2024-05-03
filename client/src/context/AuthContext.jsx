import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { baseUrl, postRequest } from "../utils/services";
const AuthContext = createContext();
export const AuthContextProvider = ({ children }) => {
  //user state
  const [user, setUser] = useState(null);
  //keep track of user object in local storage
  useEffect(() => {
    const user = localStorage.getItem("User");
    setUser(JSON.parse(user));
  }, []);

  //logging states
  const [loginInfo, setLoginInfo] = useState({
    email: "",
    password: "",
  });
  const [loginError, setLoginError] = useState(null);
  const [isLoginLoading, setIsLoginLoading] = useState(false);

  //update login info
  const updateLoginInfo = useCallback((info) => {
    setLoginInfo(info);
  }, []);
  //login function
  const login = useCallback(
    async (e) => {
      e.preventDefault();
      setIsLoginLoading(true);
      setLoginError(null);
      const response = await postRequest(
        `${baseUrl}/login`,
        JSON.stringify(loginInfo)
      );

      setIsLoginLoading(false);
      if (response.error) {
        return setLoginError(response);
      }
      localStorage.setItem("User", JSON.stringify(response));
      setUser(response);
    },
    [loginInfo]
  );

  //logout function (remove user item)
  const logout = useCallback(() => {
    localStorage.removeItem("User");
    setUser(null);
  }, []);

  // generate function
  const generate = useCallback(
    async (message) => {
      // Ensure user is not null before accessing token
      if (user) {
        try {
          const token = user.token;
          const headers = {
            Authorization: `Bearer ${token}`,
          };
          const response = await postRequest(
            `${baseUrl}/generate`,
            JSON.stringify({ message: message }),
            headers
          );
          return response;
        } catch (error) {
          console.error("Error:", error);
          // Handle error appropriately
        }
      }
    },
    [user]
  );
  //export values
  const value = {
    user,
    login,
    loginError,
    loginInfo,
    updateLoginInfo,
    isLoginLoading,
    logout,
    generate,
  };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};

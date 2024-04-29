import { Link } from "react-router-dom";

const ErrorPage = () => {
  return (
    <div>
      Error: Page not Found
      <Link to="/english-teacher-website">Back to home page</Link>
    </div>
  );
};

export default ErrorPage;

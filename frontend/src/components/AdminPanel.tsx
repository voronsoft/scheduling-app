import { Link } from "react-router-dom";

const AdminPanel = () => {
  return (
    <div>
      Admin Panel will appear here
      <br />
      <Link to="/english-teacher-website" className="cursor-pointer">
        Back to home page
      </Link>
    </div>
  );
};

export default AdminPanel;

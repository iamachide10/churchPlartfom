import { useAuth } from "../context/AuthContext";
import { FaFacebook, FaTwitter, FaYoutube } from "react-icons/fa";
import { logInNavLinks,logOutNavLinks } from "../Constant";


const Footer = () => {
  const {user}=useAuth();

  const NavList=user?logInNavLinks:logOutNavLinks;
  return (
    <footer className="bg-black text-gray-300 py-10 px-6 mt-10 ">
      <div className="max-w-7xl mx-auto grid gap-8 md:grid-cols-3 text-center md:text-left">
        
        {/* Logo / App Name */}
        <div>
          <h2 className="text-2xl font-bold text-yellow-400">Min. Elistar Ministry</h2>
          <p className="mt-2 text-sm">
            Bringing the Word of God closer to you, anytime and anywhere.
          </p>
        </div>

        {/* Quick Links */}
        <div>
          <h3 className="text-lg font-semibold text-yellow-400 mb-3">Quick Links</h3>
          <ul className="space-y-2">
            {NavList.map(item=>(
            <li><a href={item.href} className="hover:text-yellow-400">{item.name}</a></li>
            ))}
          </ul>
        </div>

        {/* Social Media */}
        <div>
          <h3 className="text-lg font-semibold text-yellow-400 mb-3">Follow Us</h3>
          <div className="flex justify-center md:justify-start space-x-4">
            <a href="#"><FaFacebook className="text-2xl hover:text-yellow-400" /></a>
            <a href="#"><FaTwitter className="text-2xl hover:text-yellow-400" /></a>
            <a href="#"><FaYoutube className="text-2xl hover:text-yellow-400" /></a>
          </div>
        </div>
      </div>

      {/* Bottom Line */}
      <div className="mt-8 border-t border-gray-700 pt-4 text-center text-sm">
        © {new Date().getFullYear()} Min. Elistar Ministry. All rights reserved.
      </div>
    </footer>
  );
};

export default Footer;

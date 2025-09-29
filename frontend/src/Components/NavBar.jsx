import { NavLink } from "react-router-dom";
import { logInNavLinks } from "../Constant";
import { logOutNavLinks } from "../Constant";
import myImage from "../assets/logo.jpg";
import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { useAuth } from "../context/AuthContext";


export default function NavBar() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const {user}=useAuth();    

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const NavList = user? logInNavLinks :logOutNavLinks;


  return (
    <header
      className={`fixed top-0 left-0 w-full z-50 transition-colors duration-300 ${
        scrolled ? "bg-black/70 backdrop-blur-md" : "bg-black"
      }`}
    >
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-4">
          {/* Logo */}
          <a href="/" className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-full flex items-center justify-center bg-yellow-400 text-black font-bold">
              <img className="h-9 w-9 rounded-full" src={myImage} alt="logo" />
            </div>
            <span className="text-lg font-semibold text-yellow-400">MEM</span>
          </a>

          {/* Right side */}
          <div className="relative flex items-center gap-4">
            {/* Desktop links */}
            <div className="hidden md:flex items-center gap-6">
              {NavList.map((nav) => (
                <NavLink
                  key={nav.id}
                  to={nav.href}
                  className={({ isActive }) =>
                    `block px-4 py-2 rounded-md ${
                      isActive
                        ? "bg-yellow-400 text-black font-semibold"
                        : "text-gray-200 hover:text-yellow-300 hover:bg-gray-800"
                    }`
                  }
                >
                  {nav.name}
                </NavLink>
              ))}
              {user && <span className="text-gray-300">Hello, {user.name}</span>}
            </div>

            {/* Mobile button */}
            <button
              onClick={() => setOpen((v) => !v)}
              aria-expanded={open}
              aria-controls="mobile-menu"
              className="md:hidden p-2 rounded-md text-gray-300 hover:bg-gray-800"
            >
              {open ? (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              ) : (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg> 
              )}
            </button>

            {/* Mobile dropdown */}
            {open && (
              <div
                id="mobile-menu"
                role="menu"
                className="absolute sm:w-full right-0 top-full mt-2 w-48 rounded-md bg-black/90 backdrop-blur-sm border border-gray-800 shadow-lg md:hidden"
              >
                {NavList.map((nav) => (
                  <NavLink
                    key={nav.id}
                    to={nav.href}
                    onClick={() => setOpen(false)} // close menu after click
                    className={({ isActive }) =>
                      `block px-4 py-2 rounded-md ${
                        isActive
                          ? "bg-yellow-400 text-black font-semibold"
                          : "text-gray-200 hover:text-yellow-300 hover:bg-gray-800"
                      }`
                    }
                  >
                    {nav.name}
                  </NavLink>
                ))}
                {user && <span className="block px-4 py-2 text-gray-300">Hello, {user.name}</span>}
              </div>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}

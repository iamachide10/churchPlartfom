import { UploadSermonTrial } from "./Trial";
import NavBar from "../Components/NavBar"; 
import { SermonListPage } from "./SermonListPage"; 
import Footer from "../Components/Footer";
import LandingPage from "./LandingPage";
import {Routes, Route , Link} from "react-router-dom"
import SignIn from "./SignInPage";
import SignUp from "./sign_page";
import AboutUs from "./AboutUsPage";
import SermonPackDetails from "./SermonPackDetail";
import UploadSermon from "./UploadSermon";




export const Main =()=>{

    return(<div>
        <NavBar/>
        <Routes>
            <Route path="/" element={<LandingPage/>}/>
            <Route path="/upload" element={<UploadSermonTrial />} />
            <Route path="/sermons/:id" element={<SermonPackDetails />} />
            <Route path="/sign_in" element={<SignIn/>}/>
            <Route path="/sermons" element={<SermonListPage/>}/>
            <Route path="/sign_up" element={<SignUp/>}/>
            <Route path="/about_us" element={<AboutUs/>}/>
        </Routes>
        <Footer/>
    </div>)
}
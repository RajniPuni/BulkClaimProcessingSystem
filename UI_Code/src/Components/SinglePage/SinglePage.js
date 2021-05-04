import React, { useState } from 'react';
import Navbar from './NavBar/Navbar';
import Opening from './Opening/Opening';
import Sidebar from './SideBar/SideBar';
import About from './About/About';
import homeObjOne from './About/Data1';
import homeObjTwo from './About/Data2';
import homeObjThree from './About/Data3';
import Service from './Services/Service';
import Footer from './Footer/Footer';
import Chart from './Chart/Chart';

const SinglePage = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggle = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className="wrapper">
            {/* <Sidebar isOpen={isOpen} toggle={toggle} />
            <Navbar toggle={toggle} /> */}
            <Opening />
            <About {...homeObjOne}/>
            <About {...homeObjTwo} />
            <Service />
            <About {...homeObjThree} />
            {/* <Chart/> */}
            <Footer />
        </div>        
    );
};

export default SinglePage
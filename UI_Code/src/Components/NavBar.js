import React, { Component } from "react";
import { Navbar, Nav } from 'react-bootstrap';

class NavBar extends Component {
    render() {
        return (
            <Navbar bg="primary" variant="dark">
                <Navbar.Brand href="/">CPU</Navbar.Brand>
                <Nav className="mr-auto">
                    <Nav.Link href="/">Home</Nav.Link>
                    <Nav.Link href="/uploadfile">Upload File</Nav.Link>
                    <Nav.Link href="/SignUp">Register</Nav.Link>
                </Nav>
            </Navbar>
        )
    }
};
export default NavBar;
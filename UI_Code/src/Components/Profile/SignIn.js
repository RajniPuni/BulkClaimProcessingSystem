import React, { Component } from "react";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBInput,
  MDBBtn,
  MDBCard,
  MDBCardBody,
  MDBLink,
} from "mdbreact";
import { Link } from "react-router-dom";
import Fade from "react-reveal/Fade";
import img from "../img.png";
import NavBar from "../NavBar";

class SignIn extends Component {
  constructor() {
    super();
    this.state = {
      email: "",
      password: "",
      errors: {},
      valid: false,
      security: "",
    };
    this.onSubmit = this.onSubmit.bind(this);
  }

  onSubmit(e) {
    e.preventDefault();
    this.onFormSubmit(e);
    if (this.state.valid) {
      this.props.history.push(`/uploadfile`);
    }
  }

  onFormSubmit = (e) => {
    e.preventDefault();
    const { email, password } = this.state;
    const validEmailRegex = RegExp(
      /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
    );
    if (!validEmailRegex.test(email)) {
      alert("Type a valid email id");
    } else if (password.length < 5) {
      alert("Password should be of atleast 5 characters length");
    } else {
      this.setState({ valid: true });
    }
  };

  getLoginData = (value, type) =>
    this.setState({
      [type]: value,
    });

  render() {
    return (
      <div
        style={{
          backgroundImage: `url(${img})`,
          backgroundPosition: "center",
          backgroundRepeat: "no - repeat",
          backgroundSize: "cover",
        }}
      >
        <NavBar/>
        <Fade left>
          <MDBContainer className="p-5">
            <MDBRow className="d-flex justify-content-center">
              <MDBCol md="6">
                <MDBCard>
                  <div className="header pt-3 blue-gradient">
                    <MDBRow className="d-flex justify-content-center">
                      <h3 className="white-text mb-3 pt-3 font-weight-bold">
                        Sign in
                      </h3>
                    </MDBRow>
                  </div>
                  <MDBCardBody>
                    <form noValidate>
                      <div className="grey-text">
                        <MDBInput
                          label="Type your email"
                          icon="envelope"
                          gup
                          type="text"
                          validate
                          required
                          getValue={(value) =>
                            this.getLoginData(value, "email")
                          }
                        />
                        <MDBInput
                          label="Your password"
                          icon="lock"
                          group
                          type="password"
                          validate
                          containerClass="mb-0"
                          getValue={(value) =>
                            this.getLoginData(value, "password")
                          }
                        />
                        <MDBInput
                          label="Your favourite school teacher name"
                          icon="lock"
                          group
                          type="text"
                          validate
                          containerClass="mb-0"
                          getValue={(value) =>
                            this.getLoginData(value, "security")
                          }
                        />

                        <h5 className="font-small blue-text d-flex justify-content-end pb-2">
                          Forgot
                          <Link to="/Resetpassword" className="blue-text ml-1">
                            Password?
                          </Link>
                        </h5>
                        <div className="text-center">
                          New User?<MDBLink to="/SignUp">Sign Up</MDBLink>
                        </div>
                      </div>
                      <div className="text-center py-3 mt-3">
                        <MDBBtn
                          type="button"
                          gradient="blue"
                          className="btn-block z-depth-1a white-text font-weight-bold"
                          onClick={this.onSubmit}
                        >
                          Sign in
                        </MDBBtn>
                      </div>
                    </form>
                  </MDBCardBody>
                </MDBCard>
              </MDBCol>
            </MDBRow>
          </MDBContainer>
        </Fade>
      </div>
    );
  }
}

export default SignIn;

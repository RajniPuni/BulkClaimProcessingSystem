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
    const { username, password, email, confirmemail } = this.state;
    const validEmailRegex = RegExp(
      /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
    );
    const validName = RegExp(/^([\w]{3,})+\s+([\w\s]{3,})+$/i);
    if (!validEmailRegex.test(email)) {
      alert("Type a valid email id");
    } else if (password.length < 5) {
      alert("Password should be of atleast 5 characters length");
    } else if (email !== confirmemail) {
      alert("Email id does not match");
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
                        Sign Up
                      </h3>
                    </MDBRow>
                  </div>
                  <MDBCardBody>
                    <form noValidate onSubmit={this.onSubmit}>
                      <div className="grey-text">
                        <MDBInput
                          label="Your full name"
                          icon="user"
                          group
                          type="text"
                          validate
                          getValue={(value) =>
                            this.getLoginData(value, "username")
                          }
                        />
                        <MDBInput
                          label="Your email"
                          icon="envelope"
                          group
                          type="email"
                          validate
                          getValue={(value) =>
                            this.getLoginData(value, "email")
                          }
                        />
                        <MDBInput
                          label="Confirm your email"
                          icon="exclamation-triangle"
                          group
                          type="email"
                          validate
                          getValue={(value) =>
                            this.getLoginData(value, "confirmemail")
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

                        <div className="text-center">
                          Already Registered?
                          <MDBLink to="/">Sign In</MDBLink>
                        </div>
                        <div className="text-center">
                          <MDBBtn
                            type="submit"
                            gradient="blue"
                            className="btn-block z-depth-1a white-text font-weight-bold"
                            onClick={this.onSubmit}
                          >
                            Register
                          </MDBBtn>
                        </div>
                      </div>
                    </form>
                  </MDBCardBody>
                </MDBCard>
              </MDBCol>
            </MDBRow>
                </MDBContainer>
                <br />
        </Fade>
      </div>
    );
  }
}

export default SignIn;

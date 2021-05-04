import React, { useState} from 'react';
import { OpeningContainer, OpenBg, VideoBg, OpenContent, OpenH1, OpenP, OpenBtnWrapper, ArrowForward, ArrowRight } from './OpeningElements';
import Video from '../../Video/video.mp4';
import { Button } from '../ButtonElement';

const Opening = () => {

    const [hover, setHover] = useState(false)

    const onHover = () => {
        setHover(!hover)
    }
        return (
            <OpeningContainer id='home'>
                <OpenBg>
                    <VideoBg autoPlay loop muted src={Video} type='video/mp4'/>
                </OpenBg>
                <OpenContent>
                    <OpenH1>Insurance coverage made easy</OpenH1>
                    <OpenP>
                        Claim your Insurance now with a click.
                    </OpenP>
                    <OpenBtnWrapper>
                        <Button to='signup' onMouseEnter={onHover} onMouseLeave={onHover} primary='true' dark='true' smooth={true} duration={500} spy={true} exact='true' offset={-80}>
                            Claim Up {hover ? <ArrowForward/> : <ArrowRight/>}
                        </Button>
                    </OpenBtnWrapper>
                </OpenContent>
            </OpeningContainer>
        );
    
}

export default Opening;
# SHUC

## Description

**SHUC** (an Amharic word for whisper) is a home companion robot. It has autonomous navigation capabilities (SLAM + A* path planner) and can interact with people via voice commands. SHUC has a visual attention system that was largely inspired by Professor Cynthia Brazil's work on Kismet robot. SHUC's visual attention system combines bottom-up features like motions in the environment and skin color with top-down features like faces to generate a saliency map. The saliency map is then used for guiding SHUC towards interesting regions in its field of view. Besides voice commands, users can interact with SHUC through a custom built android app. The entire system was built on top of ROS and costs less than 250 USD.

<p align="center">
  <img src="https://github.com/danenigma/SHUC/blob/master/shuc-final.png">
</p>

## Overall System Architecture
<p align="center">
  <img src="https://github.com/danenigma/SHUC/blob/master/overall-sys.png">
</p>

## Frame

<p align="center">
  <img src="https://github.com/danenigma/SHUC/blob/master/shuc_frame.jpg">
  <img width="369" height="363" src="https://github.com/danenigma/SHUC/blob/master/shuc-labeled.jpg">
</p>

## Android Application

<p align="center">
  <img width="369" height="305" src="https://github.com/danenigma/SHUC/blob/master/shuc-nav-app.png">
  <img width="369" height="305" src="https://github.com/danenigma/SHUC/blob/master/shuc-vid-stream.png">
</p>


## Body Design

<p align="center">
  <img width="369" height="363"  src="https://github.com/danenigma/SHUC/blob/master/shuc_body_design.jpg">
</p>

## Demo
[SHUC eyes](https://www.youtube.com/watch?v=kLXe7wfBn30)
[SHUC neck](https://www.youtube.com/watch?v=W1nFgOfRG8w)
[SHUC performing SLAM](https://www.youtube.com/watch?v=DXvhSlTFk2I)

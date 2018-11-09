# SHUC

**SHUC** (an Amharic word for whisper) is a home companion robot. It has autonomous navigation capabilities (SLAM + A* path planner) and can interact with people via voice commands. SHUC has a visual attention system that was largely inspired by Professor Cynthia Brazil's work on Kismet robot. SHUC's visual attention system combines bottom-up features like motions in the environment and skin color with top-down features like faces to generate a saliency map. The saliency map is then used for guiding SHUC towards interesting regions in its field of view. Besides voice commands, users can interact with SHUC through a custom built android app. The entire system was built on top of ROS and costs less than 250 USD.

![alt text](https://github.com/danenigma/SHUC/blob/master/shuc-final.png)
<p align="center">
  <img width="460" height="300" src="https://github.com/danenigma/SHUC/blob/master/shuc-final.png">
</p>

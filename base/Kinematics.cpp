//
// Created by Chen on 2018/11/19.
//
#include "Kinematics.h"

extern "C"
Pos Kinematics(float* angles)
{
    RobotDimensions dimensions;

    Pose3D rel_parts[BodyPart::NUM_PARTS];
    // right shoulder
    BodyPart::Part shoulder = BodyPart::right_shoulder;
    Joint arm0 = RShoulderPitch;
    rel_parts[BodyPart::torso] = Pose3D(0, 0, 0).translate(0, 0, dimensions.upperLegLength+
                                                                 dimensions.lowerLegLength+
                                                                 dimensions.footHeight);

    rel_parts[shoulder + 0] = Pose3D(rel_parts[BodyPart::torso])
            .translate(dimensions.armOffset.x, dimensions.armOffset.y * -1, dimensions.armOffset.z)
            .rotateY(-angles[arm0 + 0]);
    rel_parts[shoulder + 1] = Pose3D(rel_parts[shoulder + 0])
            .rotateZ(angles[arm0 + 1] * -1);
    rel_parts[shoulder + 2] = Pose3D(rel_parts[shoulder + 1])
            .translate(dimensions.upperArmLength, 0, 0)
            .rotateX(angles[arm0 + 2]);
    rel_parts[shoulder + 3] = Pose3D(rel_parts[shoulder + 2])
            .rotateZ(angles[arm0 + 3] * -1)
            .translate(dimensions.lowerArmLength, 0, 0);

    Vector3<float> res = rel_parts[shoulder + 3].rotation * Vector3<float>(0, 0, 0) + rel_parts[shoulder + 3].translation;
    Pos pos;
    pos.x = res.x;
    pos.y = res.y;
    pos.z = res.z;
    return pos;
}
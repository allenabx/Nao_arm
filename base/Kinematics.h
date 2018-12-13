//
// Created by Chen on 2018/11/19.
//

#ifndef C_KINEMATICS_H
#define C_KINEMATICS_H

#include <iostream>
#include "RotationMatrix.h"
#include "Pose3D.h"
#include "RobotDimensions.h"

using namespace std;

//# define M_E		2.7182818284590452354	/* e */
//# define M_LOG2E	1.4426950408889634074	/* log_2 e */
//# define M_LOG10E	0.43429448190325182765	/* log_10 e */
//# define M_LN2		0.69314718055994530942	/* log_e 2 */
//# define M_LN10		2.30258509299404568402	/* log_e 10 */
//# define M_PI		3.14159265358979323846	/* pi */
//# define M_PI_2		1.57079632679489661923	/* pi/2 */
//# define M_PI_4		0.78539816339744830962	/* pi/4 */
//# define M_1_PI		0.31830988618379067154	/* 1/pi */
//# define M_2_PI		0.63661977236758134308	/* 2/pi */
//# define M_2_SQRTPI	1.12837916709551257390	/* 2/sqrt(pi) */
//# define M_SQRT2	1.41421356237309504880	/* sqrt(2) */
//# define M_SQRT1_2	0.70710678118654752440	/* 1/sqrt(2) */


namespace BodyPart {
    enum Part {
        neck,
        head,
        left_shoulder,
        left_bicep,
        left_elbow,
        left_forearm,
        right_shoulder,
        right_bicep,
        right_elbow,
        right_forearm,
        left_pelvis,
        left_hip,
        left_thigh,
        left_tibia,
        left_ankle,
        left_foot, // rotated at ankle (used for weight)
        left_bottom_foot, // translated (used for pose)
        right_pelvis,
        right_hip,
        right_thigh,
        right_tibia,
        right_ankle,
        right_foot,
        right_bottom_foot,
        torso,
        NUM_PARTS
    };
}

enum Joint {
    HeadYaw = 0,
    HeadPitch = 1,

    LHipYawPitch = 2,
    LHipRoll = 3,
    LHipPitch = 4,
    LKneePitch = 5,
    LAnklePitch = 6,
    LAnkleRoll = 7,

    RHipYawPitch = 8,
    RHipRoll = 9,
    RHipPitch = 10,
    RKneePitch = 11,
    RAnklePitch = 12,
    RAnkleRoll = 13,

    LShoulderPitch = 14,
    LShoulderRoll = 15,
    LElbowYaw = 16,
    LElbowRoll = 17,

    RShoulderPitch = 18,
    RShoulderRoll = 19,
    RElbowYaw = 20,
    RElbowRoll = 21,

    LToePitch = 22,
    RToePitch = 23,

    NUM_JOINTS = 24
};


//Joint JointMapByJointId[] = {
//        HeadYaw,
//        HeadPitch,
//
//        LShoulderPitch,
//        RShoulderPitch,
//        LShoulderRoll,
//        RShoulderRoll,
//        LElbowYaw,
//        RElbowYaw,
//        LElbowRoll,
//        RElbowRoll,
//
//        LHipYawPitch,
//        RHipYawPitch,
//        LHipRoll,
//        RHipRoll,
//        LHipPitch,
//        RHipPitch,
//        LKneePitch,
//        RKneePitch,
//        LAnklePitch,
//        RAnklePitch,
//        LAnkleRoll,
//        RAnkleRoll,
//};
//
//JointID JointIDMapByJoint[] = {
//        JID_HEAD_1,
//        JID_HEAD_2,
//
//        JID_LLEG_1,
//        JID_LLEG_2,
//        JID_LLEG_3,
//        JID_LLEG_4,
//        JID_LLEG_5,
//        JID_LLEG_6,
//
//        JID_RLEG_1,
//        JID_RLEG_2,
//        JID_RLEG_3,
//        JID_RLEG_4,
//        JID_RLEG_5,
//        JID_RLEG_6,
//
//        JID_LARM_1,
//        JID_LARM_2,
//        JID_LARM_3,
//        JID_LARM_4,
//
//        JID_RARM_1,
//        JID_RARM_2,
//        JID_RARM_3,
//        JID_RARM_4,
//};

extern "C"
typedef struct Pos
{
    float x;
    float y;
    float z;
    float elbowx;
    float elbowy;
    float elbowz;
}Pos;

extern "C"
Pos Kinematics(float* angles);

#endif //C_KINEMATICS_H

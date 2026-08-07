class CfgPatches
{
    class Offroad_02_Tan
    {
        units[] = 
        { 
            "offroad_02_tan",
            "offroad_02_door_1_1_tan",
            "offroad_02_door_2_1_tan",
            "offroad_02_door_1_2_tan",
            "offroad_02_door_2_2_tan",
            "offroad_02_hood_tan",
            "offroad_02_trunk_tan"
        };
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] = { "DZ_Data", "DZ_Vehicles_Wheeled" };
    };
};

class CfgVehicles
{
    class Offroad_02;
    class Offroad_02_Door_1_1;
    class Offroad_02_Door_2_1;
    class Offroad_02_Door_1_2;
    class Offroad_02_Door_2_2;
    class Offroad_02_Hood;
    class Offroad_02_Trunk;

    class offroad_02_tan : Offroad_02
    {
        scope = 2;
        displayName = "Tan Humvee";
        descriptionShort = "A military offroad vehicle with a custom tan paint job.";
        
        model = "\Jordans_tan_HMMV\offroad_02_tan.p3d";

        hiddenSelectionsTextures[] = 
        {
            "Jordans_tan_HMMV\data\offroad_02_tan_co.paa"
        };
    };

    class offroad_02_door_1_1_tan : Offroad_02_Door_1_1
    {
        scope = 2;
        displayName = "Tan Humvee Front Left Door";
        descriptionShort = "A tan painted front left door for the Humvee.";
        hiddenSelectionsTextures[] = { "Jordans_tan_HMMV\data\offroad_02_tan_co.paa" };
    };

    class offroad_02_door_2_1_tan : Offroad_02_Door_2_1
    {
        scope = 2;
        displayName = "Tan Humvee Front Right Door";
        descriptionShort = "A tan painted front right door for the Humvee.";
        hiddenSelectionsTextures[] = { "Jordans_tan_HMMV\data\offroad_02_tan_co.paa" };
    };

    class offroad_02_door_1_2_tan : Offroad_02_Door_1_2
    {
        scope = 2;
        displayName = "Tan Humvee Rear Left Door";
        descriptionShort = "A tan painted rear left door for the Humvee.";
        hiddenSelectionsTextures[] = { "Jordans_tan_HMMV\data\offroad_02_tan_co.paa" };
    };

    class offroad_02_door_2_2_tan : Offroad_02_Door_2_2
    {
        scope = 2;
        displayName = "Tan Humvee Rear Right Door";
        descriptionShort = "A tan painted rear right door for the Humvee.";
        hiddenSelectionsTextures[] = { "Jordans_tan_HMMV\data\offroad_02_tan_co.paa" };
    };

    class offroad_02_hood_tan : Offroad_02_Hood
    {
        scope = 2;
        displayName = "Tan Humvee Hood";
        descriptionShort = "A tan painted hood for the Humvee.";
        hiddenSelectionsTextures[] = { "Jordans_tan_HMMV\data\offroad_02_tan_co.paa" };
    };

    class offroad_02_trunk_tan : Offroad_02_Trunk
    {
        scope = 2;
        displayName = "Tan Humvee Trunk";
        descriptionShort = "A tan painted trunk door for the Humvee.";
        hiddenSelectionsTextures[] = { "Jordans_tan_HMMV\data\offroad_02_tan_co.pyy" }; 
    };
};
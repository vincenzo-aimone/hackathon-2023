<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.10.2" name="arcade_platformer" tilewidth="128" tileheight="128" tilecount="128" columns="0">
 <editorsettings>
  <export target="arcade_platformer.tsx" format="tsx"/>
 </editorsettings>
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0">
  <image width="128" height="128" source="images/ground/Grass/grass.png"/>
 </tile>
 <tile id="1">
  <image width="128" height="128" source="images/ground/Grass/grassCenter_round.png"/>
 </tile>
 <tile id="2">
  <image width="128" height="128" source="images/ground/Grass/grassCenter.png"/>
 </tile>
 <tile id="3">
  <image width="128" height="128" source="images/ground/Grass/grassCliff_left.png"/>
 </tile>
 <tile id="4">
  <image width="128" height="128" source="images/ground/Grass/grassCliff_right.png"/>
 </tile>
 <tile id="5">
  <image width="128" height="128" source="images/ground/Grass/grassCliffAlt_left.png"/>
 </tile>
 <tile id="6">
  <image width="128" height="128" source="images/ground/Grass/grassCliffAlt_right.png"/>
 </tile>
 <tile id="7">
  <image width="128" height="128" source="images/ground/Grass/grassCorner_left.png"/>
 </tile>
 <tile id="8">
  <image width="128" height="128" source="images/ground/Grass/grassCorner_right.png"/>
 </tile>
 <tile id="9">
  <image width="128" height="128" source="images/ground/Grass/grassHalf_left.png"/>
 </tile>
 <tile id="10">
  <image width="128" height="128" source="images/ground/Grass/grassHalf_mid.png"/>
 </tile>
 <tile id="11">
  <image width="128" height="128" source="images/ground/Grass/grassHalf_right.png"/>
 </tile>
 <tile id="12">
  <image width="128" height="128" source="images/ground/Grass/grassHalf.png"/>
 </tile>
 <tile id="13">
  <image width="128" height="128" source="images/ground/Grass/grassHill_left.png"/>
  <objectgroup draworder="index">
   <object id="2" x="0.545455" y="0.909091">
    <polygon points="-0.545455,-0.909091 127.455,127.091 -0.545455,127.091"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="14">
  <image width="128" height="128" source="images/ground/Grass/grassHill_right.png"/>
  <objectgroup draworder="index">
   <object id="1" x="0" y="128">
    <polygon points="0,0 128,0 128,-128"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="15">
  <image width="128" height="128" source="images/ground/Grass/grassLeft.png"/>
 </tile>
 <tile id="16">
  <image width="128" height="128" source="images/ground/Grass/grassMid.png"/>
 </tile>
 <tile id="17">
  <image width="128" height="128" source="images/ground/Grass/grassRight.png"/>
 </tile>
 <tile id="29">
  <image width="128" height="128" source="images/HUD/hudHeart_empty.png"/>
 </tile>
 <tile id="30">
  <image width="128" height="128" source="images/HUD/hudHeart_full.png"/>
 </tile>
 <tile id="33">
  <image width="128" height="128" source="images/HUD/hudJewel_blue.png"/>
 </tile>
 <tile id="35">
  <image width="128" height="128" source="images/HUD/hudJewel_green.png"/>
 </tile>
 <tile id="37">
  <image width="128" height="128" source="images/HUD/hudJewel_red.png"/>
 </tile>
 <tile id="39">
  <image width="128" height="128" source="images/HUD/hudJewel_yellow.png"/>
 </tile>
 <tile id="41">
  <image width="128" height="128" source="images/HUD/hudKey_blue.png"/>
 </tile>
 <tile id="43">
  <image width="128" height="128" source="images/HUD/hudKey_green.png"/>
 </tile>
 <tile id="45">
  <image width="128" height="128" source="images/HUD/hudKey_red.png"/>
 </tile>
 <tile id="47">
  <image width="128" height="128" source="images/HUD/hudKey_yellow.png"/>
 </tile>
 <tile id="53">
  <image width="128" height="128" source="images/HUD/hudX.png"/>
 </tile>
 <tile id="54">
  <properties>
   <property name="point_value" type="int" value="5"/>
  </properties>
  <image width="128" height="128" source="images/items/coinBronze.png"/>
 </tile>
 <tile id="55">
  <properties>
   <property name="point_value" type="int" value="20"/>
  </properties>
  <image width="128" height="128" source="images/items/coinGold.png"/>
 </tile>
 <tile id="56">
  <properties>
   <property name="point_value" type="int" value="10"/>
  </properties>
  <image width="128" height="128" source="images/items/coinSilver.png"/>
 </tile>
 <tile id="60">
  <image width="128" height="128" source="images/items/flagGreen_down.png"/>
 </tile>
 <tile id="61">
  <image width="128" height="128" source="images/items/flagGreen1.png"/>
  <animation>
   <frame tileid="61" duration="250"/>
   <frame tileid="62" duration="250"/>
  </animation>
 </tile>
 <tile id="62">
  <image width="128" height="128" source="images/items/flagGreen2.png"/>
 </tile>
 <tile id="69">
  <image width="128" height="128" source="images/items/gemBlue.png"/>
 </tile>
 <tile id="70">
  <image width="128" height="128" source="images/items/gemGreen.png"/>
 </tile>
 <tile id="71">
  <image width="128" height="128" source="images/items/gemRed.png"/>
 </tile>
 <tile id="72">
  <image width="128" height="128" source="images/items/gemYellow.png"/>
 </tile>
 <tile id="77">
  <image width="128" height="128" source="images/items/star.png"/>
 </tile>
 <tile id="84">
  <image width="128" height="128" source="images/tiles/boxCrate_double.png"/>
 </tile>
 <tile id="95">
  <image width="128" height="128" source="images/tiles/brickBrown.png"/>
 </tile>
 <tile id="96">
  <image width="128" height="128" source="images/tiles/brickGrey.png"/>
 </tile>
 <tile id="104">
  <image width="128" height="128" source="images/tiles/doorOpen_mid.png"/>
 </tile>
 <tile id="105">
  <image width="128" height="128" source="images/tiles/doorOpen_top.png"/>
 </tile>
 <tile id="106">
  <image width="128" height="128" source="images/tiles/fence.png"/>
 </tile>
 <tile id="107">
  <image width="128" height="128" source="images/tiles/fenceBroken.png"/>
 </tile>
 <tile id="108">
  <image width="128" height="128" source="images/tiles/grass.png"/>
 </tile>
 <tile id="109">
  <image width="128" height="128" source="images/tiles/ladderMid.png"/>
 </tile>
 <tile id="110">
  <image width="128" height="128" source="images/tiles/ladderTop.png"/>
 </tile>
 <tile id="111">
  <image width="128" height="128" source="images/tiles/lava.png"/>
 </tile>
 <tile id="112">
  <image width="128" height="128" source="images/tiles/lavaTop_high.png"/>
 </tile>
 <tile id="113">
  <image width="128" height="128" source="images/tiles/lavaTop_low.png"/>
 </tile>
 <tile id="126">
  <image width="128" height="128" source="images/tiles/signExit.png"/>
 </tile>
 <tile id="127">
  <image width="128" height="128" source="images/tiles/signLeft.png"/>
 </tile>
 <tile id="128">
  <image width="128" height="128" source="images/tiles/signRight.png"/>
 </tile>
 <tile id="141">
  <image width="128" height="128" source="images/tiles/torch1.png"/>
 </tile>
 <tile id="142">
  <image width="128" height="128" source="images/tiles/torch2.png"/>
  <animation>
   <frame tileid="141" duration="250"/>
   <frame tileid="142" duration="250"/>
  </animation>
 </tile>
 <tile id="144">
  <image width="128" height="128" source="images/tiles/water.png"/>
 </tile>
 <tile id="145">
  <image width="128" height="128" source="images/tiles/waterTop_high.png"/>
 </tile>
 <tile id="146">
  <image width="128" height="128" source="images/tiles/waterTop_low.png"/>
 </tile>
 <tile id="150">
  <image width="128" height="128" source="images/tiles/grass2.png"/>
  <animation>
   <frame tileid="108" duration="250"/>
   <frame tileid="150" duration="250"/>
  </animation>
 </tile>
 <tile id="151">
  <image width="66" height="92" source="images/items/alienPink.png"/>
 </tile>
 <tile id="152">
  <image width="128" height="128" source="images/enemies/fly.png"/>
  <animation>
   <frame tileid="152" duration="100"/>
   <frame tileid="153" duration="100"/>
  </animation>
 </tile>
 <tile id="153">
  <image width="128" height="128" source="images/enemies/fly_dead.png"/>
 </tile>
 <tile id="154">
  <image width="128" height="128" source="images/ground/Sand/sand.png"/>
 </tile>
 <tile id="155">
  <image width="128" height="128" source="images/ground/Sand/sandCenter.png"/>
 </tile>
 <tile id="156">
  <image width="128" height="128" source="images/ground/Sand/sandCenter_rounded.png"/>
 </tile>
 <tile id="157">
  <image width="128" height="128" source="images/ground/Sand/sandCliff_left.png"/>
 </tile>
 <tile id="158">
  <image width="128" height="128" source="images/ground/Sand/sandCliff_right.png"/>
 </tile>
 <tile id="159">
  <image width="128" height="128" source="images/ground/Sand/sandCliffAlt_left.png"/>
 </tile>
 <tile id="160">
  <image width="128" height="128" source="images/ground/Sand/sandCliffAlt_right.png"/>
 </tile>
 <tile id="161">
  <image width="128" height="128" source="images/ground/Sand/sandCorner_leftg.png"/>
 </tile>
 <tile id="162">
  <image width="128" height="128" source="images/ground/Sand/sandCorner_right.png"/>
 </tile>
 <tile id="163">
  <image width="128" height="128" source="images/ground/Sand/sandHalf.png"/>
 </tile>
 <tile id="164">
  <image width="128" height="128" source="images/ground/Sand/sandHalf_left.png"/>
 </tile>
 <tile id="165">
  <image width="128" height="128" source="images/ground/Sand/sandHalf_mid.png"/>
 </tile>
 <tile id="166">
  <image width="128" height="128" source="images/ground/Sand/sandHalf_right.png"/>
 </tile>
 <tile id="167">
  <image width="128" height="128" source="images/ground/Sand/sandHill_left.png"/>
 </tile>
 <tile id="168">
  <image width="128" height="128" source="images/ground/Sand/sandHill_right.png"/>
 </tile>
 <tile id="169">
  <image width="128" height="128" source="images/ground/Sand/sandLeft.png"/>
 </tile>
 <tile id="170">
  <image width="128" height="128" source="images/ground/Sand/sandMid.png"/>
 </tile>
 <tile id="171">
  <image width="128" height="128" source="images/ground/Sand/sandRight.png"/>
 </tile>
 <tile id="172">
  <image width="128" height="128" source="images/ground/Snow/snow.png"/>
 </tile>
 <tile id="173">
  <image width="128" height="128" source="images/ground/Snow/snowCenter.png"/>
 </tile>
 <tile id="174">
  <image width="128" height="128" source="images/ground/Snow/snowCenter_rounded.png"/>
 </tile>
 <tile id="175">
  <image width="128" height="128" source="images/ground/Snow/snowCliff_left.png"/>
 </tile>
 <tile id="176">
  <image width="128" height="128" source="images/ground/Snow/snowCliff_right.png"/>
 </tile>
 <tile id="177">
  <image width="128" height="128" source="images/ground/Snow/snowCliffAlt_left.png"/>
 </tile>
 <tile id="178">
  <image width="128" height="128" source="images/ground/Snow/snowCliffAlt_right.png"/>
 </tile>
 <tile id="179">
  <image width="128" height="128" source="images/ground/Snow/snowCorner_left.png"/>
 </tile>
 <tile id="180">
  <image width="128" height="128" source="images/ground/Snow/snowCorner_right.png"/>
 </tile>
 <tile id="181">
  <image width="128" height="128" source="images/ground/Snow/snowHalf.png"/>
 </tile>
 <tile id="182">
  <image width="128" height="128" source="images/ground/Snow/snowHalf_left.png"/>
 </tile>
 <tile id="183">
  <image width="128" height="128" source="images/ground/Snow/snowHalf_mid.png"/>
 </tile>
 <tile id="184">
  <image width="128" height="128" source="images/ground/Snow/snowHalf_right.png"/>
 </tile>
 <tile id="185">
  <image width="128" height="128" source="images/ground/Snow/snowHill_left.png"/>
 </tile>
 <tile id="186">
  <image width="128" height="128" source="images/ground/Snow/snowHill_right.png"/>
 </tile>
 <tile id="187">
  <image width="128" height="128" source="images/ground/Snow/snowLeft.png"/>
 </tile>
 <tile id="188">
  <image width="128" height="128" source="images/ground/Snow/snowMid.png"/>
 </tile>
 <tile id="189">
  <image width="128" height="128" source="images/ground/Snow/snowRight.png"/>
 </tile>
 <tile id="190">
  <image width="128" height="128" source="images/tiles/snow.png"/>
 </tile>
 <tile id="191">
  <image width="128" height="128" source="images/tiles/cactus.png"/>
 </tile>
 <tile id="192">
  <image width="128" height="128" source="images/tiles/plantPurple.png"/>
 </tile>
 <tile id="193">
  <image width="128" height="128" source="images/tiles/rock.png"/>
 </tile>
 <tile id="194">
  <image width="128" height="128" source="images/ground/Planet/planet.png"/>
 </tile>
 <tile id="195">
  <image width="128" height="128" source="images/ground/Planet/planetCenter.png"/>
 </tile>
 <tile id="196">
  <image width="128" height="128" source="images/ground/Planet/planetCenter_rounded.png"/>
 </tile>
 <tile id="197">
  <image width="128" height="128" source="images/ground/Planet/planetCliff_left.png"/>
 </tile>
 <tile id="198">
  <image width="128" height="128" source="images/ground/Planet/planetCliff_right.png"/>
 </tile>
 <tile id="199">
  <image width="128" height="128" source="images/ground/Planet/planetCliffAlt_left.png"/>
 </tile>
 <tile id="200">
  <image width="128" height="128" source="images/ground/Planet/planetCliffAlt_right.png"/>
 </tile>
 <tile id="201">
  <image width="128" height="128" source="images/ground/Planet/planetCorner_left.png"/>
 </tile>
 <tile id="202">
  <image width="128" height="128" source="images/ground/Planet/planetCorner_right.png"/>
 </tile>
 <tile id="203">
  <image width="128" height="128" source="images/ground/Planet/planetHalf.png"/>
 </tile>
 <tile id="204">
  <image width="128" height="128" source="images/ground/Planet/planetHalf_left.png"/>
 </tile>
 <tile id="205">
  <image width="128" height="128" source="images/ground/Planet/planetHalf_mid.png"/>
 </tile>
 <tile id="206">
  <image width="128" height="128" source="images/ground/Planet/planetHalf_right.png"/>
 </tile>
 <tile id="207">
  <image width="128" height="128" source="images/ground/Planet/planetHill_left.png"/>
 </tile>
 <tile id="208">
  <image width="128" height="128" source="images/ground/Planet/planetHill_right.png"/>
 </tile>
 <tile id="209">
  <image width="128" height="128" source="images/ground/Planet/planetLeft.png"/>
 </tile>
 <tile id="210">
  <image width="128" height="128" source="images/ground/Planet/planetMid.png"/>
 </tile>
 <tile id="211">
  <image width="128" height="128" source="images/ground/Planet/planetRight.png"/>
 </tile>
 <tile id="212">
  <image width="128" height="128" source="images/enemies/barnacle.png"/>
  <animation>
   <frame tileid="212" duration="100"/>
   <frame tileid="213" duration="100"/>
  </animation>
 </tile>
 <tile id="213">
  <image width="128" height="128" source="images/enemies/barnacle_attack.png"/>
 </tile>
 <tile id="214">
  <image width="128" height="128" source="images/enemies/barnacle_dead.png"/>
 </tile>
 <tile id="215">
  <image width="128" height="128" source="images/enemies/ladybug.png"/>
  <animation>
   <frame tileid="216" duration="100"/>
   <frame tileid="215" duration="100"/>
  </animation>
 </tile>
 <tile id="216">
  <image width="128" height="128" source="images/enemies/ladybug_move.png"/>
 </tile>
</tileset>

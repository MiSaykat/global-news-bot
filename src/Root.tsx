import React from "react";
import { Composition } from "remotion";
import { NewsComposition } from "./scenes/NewsComposition";
import { LandscapeComposition } from "./scenes/LandscapeComposition";

export const Root: React.FC = () => {
  return (
    <>
      {/* 9:16 Vertical Shorts / Reels Format (32 seconds) */}
      <Composition
        id="NewsShorts"
        component={NewsComposition}
        durationInFrames={960}
        fps={30}
        width={1080}
        height={1920}
      />

      {/* 16:9 Landscape Widescreen Broadcast Format (32 seconds) */}
      <Composition
        id="NewsLandscape"
        component={LandscapeComposition}
        durationInFrames={960}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

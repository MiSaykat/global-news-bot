import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { theme } from "../theme";

export const BgMesh: React.FC = () => {
  const frame = useCurrentFrame();
  const d1 = Math.sin(frame / 45) * 60;
  const d2 = Math.cos(frame / 60) * 50;

  return (
    <AbsoluteFill style={{ background: theme.colors.bg, overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          width: 1400,
          height: 1400,
          borderRadius: "50%",
          top: -400,
          left: -350 + d1,
          filter: "blur(90px)",
          background: `radial-gradient(circle, ${theme.colors.bgAlt}CC, transparent 65%)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 1100,
          height: 1100,
          borderRadius: "50%",
          bottom: -350,
          right: -250 - d2,
          filter: "blur(100px)",
          background: `radial-gradient(circle, #1E1B4B66, transparent 70%)`,
        }}
      />
    </AbsoluteFill>
  );
};

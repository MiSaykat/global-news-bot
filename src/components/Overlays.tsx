import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";

export const Grade: React.FC = () => (
  <AbsoluteFill
    style={{
      background: "radial-gradient(circle at 50% 40%, rgba(56, 189, 248, 0.08), rgba(15, 23, 42, 0.28))",
      mixBlendMode: "soft-light",
      pointerEvents: "none",
    }}
  />
);

export const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      boxShadow: "inset 0 0 160px 40px rgba(0, 0, 0, 0.85)",
      pointerEvents: "none",
    }}
  />
);

export const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  const ox = (frame * 17) % 100;
  const oy = (frame * 23) % 100;

  return (
    <AbsoluteFill
      style={{
        opacity: 0.06,
        mixBlendMode: "overlay",
        pointerEvents: "none",
        backgroundImage: `radial-gradient(#FFF 1px, transparent 1px)`,
        backgroundSize: "4px 4px",
        transform: `translate(${ox}px, ${oy}px)`,
      }}
    />
  );
};

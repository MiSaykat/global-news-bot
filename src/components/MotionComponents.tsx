import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";

export const Entrance: React.FC<{
  delay?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ delay = 0, children, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const p = spring({
    frame: frame - delay,
    fps,
    config: theme.spring.smooth,
  });

  return (
    <div
      style={{
        opacity: interpolate(p, [0, 1], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }),
        transform: `translateY(${interpolate(p, [0, 1], [40, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })}px) scale(${interpolate(p, [0, 1], [0.94, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })})`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

export const WordReveal: React.FC<{
  text: string;
  delay?: number;
  per?: number;
  highlightWord?: string;
  fontSize?: number;
}> = ({ text, delay = 0, per = 3, highlightWord, fontSize = 60 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: 14,
        padding: "0 40px",
      }}
    >
      {words.map((word, i) => {
        const p = spring({
          frame: frame - delay - i * per,
          fps,
          config: theme.spring.snappy,
        });

        const isHighlight =
          highlightWord &&
          word.toLowerCase().includes(highlightWord.toLowerCase());

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              opacity: interpolate(p, [0, 1], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
              transform: `translateY(${interpolate(p, [0, 1], [30, 0], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })}px) scale(${interpolate(p, [0, 1], [0.88, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
              fontSize,
              fontWeight: 800,
              letterSpacing: "-0.03em",
              fontFamily: theme.fonts.display,
              color: isHighlight ? theme.colors.primary : theme.colors.text,
              textShadow: "0 4px 16px rgba(0,0,0,0.9)",
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

export const BreakingBadge: React.FC<{ category: string }> = ({ category }) => {
  const frame = useCurrentFrame();
  const pulse = Math.sin(frame / 6) * 0.4 + 0.6;

  return (
    <div
      style={{
        position: "absolute",
        top: 90,
        left: 0,
        right: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 45px",
        height: 105,
        background: "rgba(15, 23, 42, 0.95)",
        borderBottom: `4px solid ${theme.colors.primary}`,
        boxShadow: "0 10px 30px rgba(0,0,0,0.6)",
        zIndex: 50,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            background: theme.colors.danger,
            padding: "10px 20px",
            borderRadius: 10,
          }}
        >
          <div
            style={{
              width: 14,
              height: 14,
              borderRadius: "50%",
              background: "#FFF",
              opacity: pulse,
            }}
          />
          <span
            style={{
              color: "#FFF",
              fontWeight: 800,
              fontSize: 26,
              fontFamily: theme.fonts.display,
              letterSpacing: "0.04em",
            }}
          >
            BREAKING
          </span>
        </div>

        <span
          style={{
            color: theme.colors.text,
            fontWeight: 700,
            fontSize: 26,
            fontFamily: theme.fonts.display,
            letterSpacing: "0.03em",
          }}
        >
          {category.toUpperCase()}
        </span>
      </div>

      <div
        style={{
          color: theme.colors.accent,
          fontSize: 22,
          fontWeight: 700,
          fontFamily: theme.fonts.display,
          background: "rgba(56, 189, 248, 0.12)",
          padding: "6px 14px",
          borderRadius: 8,
          border: `1px solid ${theme.colors.accent}`,
        }}
      >
        USA WIRE
      </div>
    </div>
  );
};

export const SourceCredit: React.FC<{ sourceName: string }> = ({
  sourceName,
}) => (
  <div
    style={{
      position: "absolute",
      bottom: 50,
      left: 50,
      background: "rgba(0, 0, 0, 0.7)",
      backdropFilter: "blur(8px)",
      borderLeft: `3px solid ${theme.colors.accent}`,
      padding: "6px 14px",
      borderRadius: "0 6px 6px 0",
      color: theme.colors.textDim,
      fontSize: 18,
      fontWeight: 600,
      fontFamily: theme.fonts.body,
      zIndex: 50,
    }}
  >
    FOOTAGE: {sourceName.toUpperCase()} • FAIR USE
  </div>
);

// High-Retention Outro & Call to Action (The Finishing Hook)
export const OutroCTA: React.FC<{ delay?: number }> = ({ delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({
    frame: frame - delay,
    fps,
    config: theme.spring.bouncy,
  });

  const bounce = Math.sin((frame - delay) / 5) * 6;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 28,
        width: "100%",
        maxWidth: 960,
      }}
    >
      {/* Question Card */}
      <div
        style={{
          background: "rgba(15, 23, 42, 0.95)",
          border: `3px solid ${theme.colors.primary}`,
          borderRadius: 24,
          padding: "32px 30px",
          textAlign: "center",
          boxShadow: `0 0 40px ${theme.colors.glow}`,
          transform: `scale(${interpolate(pop, [0, 1], [0.8, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })})`,
          opacity: pop,
        }}
      >
        <span
          style={{
            color: theme.colors.primary,
            fontSize: 28,
            fontWeight: 800,
            letterSpacing: "0.06em",
            display: "block",
            marginBottom: 12,
          }}
        >
          WHAT DO YOU THINK?
        </span>
        <span
          style={{
            color: "#FFF",
            fontSize: 48,
            fontWeight: 800,
            lineHeight: 1.25,
            fontFamily: theme.fonts.display,
          }}
        >
          Will AI cause nationwide power blackouts?
        </span>
      </div>

      {/* Animated Comment Box */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 16,
          background: "rgba(30, 58, 138, 0.9)",
          border: `2px solid ${theme.colors.accent}`,
          borderRadius: 50,
          padding: "16px 36px",
          transform: `translateY(${bounce}px) scale(${interpolate(pop, [0, 1], [0.85, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })})`,
          opacity: pop,
        }}
      >
        <span style={{ fontSize: 36 }}>💬</span>
        <span
          style={{
            color: "#FFF",
            fontSize: 32,
            fontWeight: 800,
            fontFamily: theme.fonts.display,
            letterSpacing: "0.02em",
          }}
        >
          DROP YOUR THOUGHTS BELOW!
        </span>
      </div>

      {/* Subscribe Pill */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          background: theme.colors.danger,
          borderRadius: 40,
          padding: "12px 30px",
          opacity: pop,
        }}
      >
        <span style={{ fontSize: 24 }}>🔔</span>
        <span
          style={{
            color: "#FFF",
            fontSize: 24,
            fontWeight: 800,
            fontFamily: theme.fonts.display,
            letterSpacing: "0.04em",
          }}
        >
          FOLLOW FOR HOURLY US BREAKING NEWS
        </span>
      </div>
    </div>
  );
};

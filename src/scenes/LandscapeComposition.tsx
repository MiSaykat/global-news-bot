import React from "react";
import {
  AbsoluteFill,
  Sequence,
  OffthreadVideo,
  Img,
  Audio,
  staticFile,
  useCurrentFrame,
  interpolate,
} from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { Grade, Vignette, Grain } from "../components/Overlays";
import {
  Entrance,
  WordReveal,
  BreakingBadge,
  SourceCredit,
} from "../components/MotionComponents";

export const LandscapeComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const totalFrames = 960; // 32 seconds at 30fps
  const progressRatio = Math.min(1, frame / totalFrames);

  return (
    <AbsoluteFill style={{ background: theme.colors.bg, overflow: "hidden" }}>
      {/* LAYER 1: Background Mesh */}
      <BgMesh />

      {/* LAYER 2: 16:9 Widescreen Media Visuals - 100% REAL MOTION VIDEO */}

      {/* CUT 1: Real B-Roll Footage 1 */}
      <Sequence from={0} durationInFrames={180}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <OffthreadVideo
            src={staticFile("footage_1.mp4")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.68) contrast(1.15)",
              transform: `scale(${interpolate(frame, [0, 180], [1.0, 1.08], {
                easing: theme.ease.inOut,
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CUT 2: Real B-Roll Footage 2 */}
      <Sequence from={180} durationInFrames={180}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <OffthreadVideo
            src={staticFile("footage_2.mp4")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.68) contrast(1.18)",
              transform: `scale(${interpolate(frame - 180, [0, 180], [1.0, 1.10], {
                easing: theme.ease.inOut,
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CUT 3: Real B-Roll Footage 3 */}
      <Sequence from={360} durationInFrames={180}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <OffthreadVideo
            src={staticFile("footage_3.mp4")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.68) contrast(1.20)",
              transform: `scale(${interpolate(frame - 360, [0, 180], [1.10, 1.0], {
                easing: theme.ease.inOut,
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CUT 4: Real B-Roll Footage 4 */}
      <Sequence from={540} durationInFrames={180}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <OffthreadVideo
            src={staticFile("footage_4.mp4")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.68) contrast(1.16)",
              transform: `scale(${interpolate(frame - 540, [0, 180], [1.0, 1.08], {
                easing: theme.ease.inOut,
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CUT 5: OUTRO BACKGROUND (Cinematic Video Background) */}
      <Sequence from={720} durationInFrames={240}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <OffthreadVideo
            src={staticFile("footage_1.mp4")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.35) blur(8px)",
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* LAYER 3: 16:9 TV Broadcast Graphics */}
      
      {/* Top Header Bar */}
      <div
        style={{
          position: "absolute",
          top: 40,
          left: 60,
          right: 60,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          background: "rgba(15, 23, 42, 0.92)",
          borderRadius: 16,
          padding: "16px 36px",
          borderBottom: `4px solid ${theme.colors.primary}`,
          zIndex: 50,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div
            style={{
              background: theme.colors.danger,
              color: "#FFF",
              fontWeight: 800,
              fontSize: 22,
              padding: "6px 18px",
              borderRadius: 8,
              letterSpacing: "0.05em",
            }}
          >
            LIVE REPORT
          </div>
          <span
            style={{
              color: "#FFF",
              fontWeight: 700,
              fontSize: 24,
              fontFamily: theme.fonts.display,
            }}
          >
            SPECIAL INVESTIGATION: US AI POWER SURGE
          </span>
        </div>
        <div
          style={{
            color: theme.colors.primary,
            fontWeight: 700,
            fontSize: 20,
            border: `1px solid ${theme.colors.primary}`,
            padding: "6px 14px",
            borderRadius: 8,
          }}
        >
          GLOBAL EDITION
        </div>
      </div>

      {/* Middle Content Captions (Frames 0 - 720) */}
      <Sequence from={5} durationInFrames={175}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <Entrance delay={5}>
            <div
              style={{
                background: "rgba(10, 15, 30, 0.90)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 20,
                padding: "28px 48px",
                maxWidth: 1400,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <WordReveal
                text="Big Tech is secretly buying nuclear power plants."
                delay={6}
                per={3}
                highlightWord="nuclear"
                fontSize={56}
              />
            </div>
          </Entrance>
        </AbsoluteFill>
      </Sequence>

      <Sequence from={185} durationInFrames={175}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <Entrance delay={185}>
            <div
              style={{
                background: "rgba(10, 15, 30, 0.90)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 20,
                padding: "28px 48px",
                maxWidth: 1400,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <WordReveal
                text="Why? Because AI is draining America's power grid at record speeds."
                delay={188}
                per={3}
                highlightWord="draining"
                fontSize={56}
              />
            </div>
          </Entrance>
        </AbsoluteFill>
      </Sequence>

      <Sequence from={365} durationInFrames={175}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <Entrance delay={365}>
            <div
              style={{
                background: "rgba(10, 15, 30, 0.90)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 20,
                padding: "28px 48px",
                maxWidth: 1400,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <WordReveal
                text="One single AI query uses 10 TIMES more power than Google."
                delay={368}
                per={3}
                highlightWord="10"
                fontSize={56}
              />
            </div>
          </Entrance>
        </AbsoluteFill>
      </Sequence>

      <Sequence from={545} durationInFrames={175}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <Entrance delay={545}>
            <div
              style={{
                background: "rgba(10, 15, 30, 0.90)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 20,
                padding: "28px 48px",
                maxWidth: 1400,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <WordReveal
                text="Microsoft and Google just inked historic multi-billion deals."
                delay={548}
                per={3}
                highlightWord="historic"
                fontSize={56}
              />
            </div>
          </Entrance>
        </AbsoluteFill>
      </Sequence>

      {/* OUTRO 16:9 BROADCAST FINISHING (Frames 725 - 960) */}
      <Sequence from={725} durationInFrames={235}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Entrance delay={728}>
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                gap: 50,
                alignItems: "center",
                background: "rgba(15, 23, 42, 0.95)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 24,
                padding: "48px 60px",
                boxShadow: `0 0 50px ${theme.colors.glow}`,
              }}
            >
              <div style={{ maxWidth: 700 }}>
                <span
                  style={{
                    color: theme.colors.primary,
                    fontSize: 24,
                    fontWeight: 800,
                    letterSpacing: "0.08em",
                    display: "block",
                    marginBottom: 10,
                  }}
                >
                  AUDIENCE POLL • YOUR VERDICT
                </span>
                <span
                  style={{
                    color: "#FFF",
                    fontSize: 44,
                    fontWeight: 800,
                    lineHeight: 1.25,
                    fontFamily: theme.fonts.display,
                  }}
                >
                  Will AI cause nationwide power blackouts in America?
                </span>
              </div>

              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: 20,
                  alignItems: "center",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 16,
                    background: "rgba(30, 58, 138, 0.95)",
                    border: `2px solid ${theme.colors.accent}`,
                    borderRadius: 40,
                    padding: "16px 36px",
                  }}
                >
                  <span style={{ fontSize: 32 }}>💬</span>
                  <span
                    style={{
                      color: "#FFF",
                      fontSize: 26,
                      fontWeight: 800,
                      fontFamily: theme.fonts.display,
                    }}
                  >
                    DROP YOUR OPINION IN COMMENTS!
                  </span>
                </div>

                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 14,
                    background: theme.colors.danger,
                    borderRadius: 40,
                    padding: "14px 36px",
                  }}
                >
                  <span style={{ fontSize: 24 }}>🔔</span>
                  <span
                    style={{
                      color: "#FFF",
                      fontSize: 22,
                      fontWeight: 800,
                      fontFamily: theme.fonts.display,
                    }}
                  >
                    SUBSCRIBE FOR FULL INVESTIGATIONS
                  </span>
                </div>
              </div>
            </div>
          </Entrance>
        </AbsoluteFill>
      </Sequence>

      {/* Bottom Ticker Bar */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 70,
          background: "rgba(10, 15, 30, 0.96)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 60px",
          borderTop: `2px solid rgba(255,255,255,0.15)`,
          zIndex: 50,
        }}
      >
        <span
          style={{
            color: theme.colors.accent,
            fontSize: 20,
            fontWeight: 700,
            fontFamily: theme.fonts.display,
          }}
        >
          TICKER: MICROSOFT THREE MILE ISLAND DEAL • GOOGLE SMR ALLIANCE • AMAZON NUCLEAR HUBS
        </span>
        <span style={{ color: theme.colors.textDim, fontSize: 18, fontWeight: 600 }}>
          FOOTAGE: OFFICIAL PRESS / VERIFIED WIRE • FAIR USE
        </span>
      </div>

      {/* Progress Line */}
      <div
        style={{
          position: "absolute",
          bottom: 70,
          left: 0,
          height: 6,
          width: `${progressRatio * 100}%`,
          background: theme.colors.primary,
          zIndex: 60,
        }}
      />

      {/* LAYER 4: Grade */}
      <Grade />

      {/* LAYER 5: Grain & Vignette */}
      <Vignette />
      <Grain />

      {/* Audio */}
      <Audio src={staticFile("voice.mp3")} />
    </AbsoluteFill>
  );
};

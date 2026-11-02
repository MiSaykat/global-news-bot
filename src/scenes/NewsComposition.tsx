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
  OutroCTA,
} from "../components/MotionComponents";

export const NewsComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const totalFrames = 960; // 32 seconds at 30fps
  const progressRatio = Math.min(1, frame / totalFrames);

  return (
    <AbsoluteFill style={{ background: theme.colors.bg, overflow: "hidden" }}>
      {/* LAYER 1: Background Mesh */}
      <BgMesh />

      {/* LAYER 2: Media & Assets (Rapid cuts every ~120 frames = 4s) */}

      {/* CUT 1 (Frames 0 - 140): Real Video Footage of Data Center */}
      <Sequence from={0} durationInFrames={140}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <OffthreadVideo
            src={staticFile("footage_1.mp4")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.72) contrast(1.15)",
              transform: `scale(${interpolate(frame, [0, 140], [1.0, 1.12], {
                easing: theme.ease.inOut,
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CUT 2 (Frames 140 - 280): Nuclear Cooling Tower Still */}
      <Sequence from={140} durationInFrames={140}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <Img
            src={staticFile("cut_2.jpg")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.70) contrast(1.2)",
              transform: `scale(${interpolate(frame - 140, [0, 140], [1.0, 1.14], {
                easing: theme.ease.inOut,
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CUT 3 (Frames 280 - 420): Microprocessor Silicon */}
      <Sequence from={280} durationInFrames={140}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <Img
            src={staticFile("cut_4.jpg")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.70) contrast(1.25)",
              transform: `scale(${interpolate(frame - 280, [0, 140], [1.14, 1.0], {
                easing: theme.ease.inOut,
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CUT 4 (Frames 420 - 560): White House / US Big Tech Deals */}
      <Sequence from={420} durationInFrames={140}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <Img
            src={staticFile("cut_3.jpg")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.70) contrast(1.2)",
              transform: `scale(${interpolate(frame - 420, [0, 140], [1.0, 1.12], {
                easing: theme.ease.inOut,
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CUT 5 (Frames 560 - 720): Electricity Blackout / Grid */}
      <Sequence from={560} durationInFrames={160}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <Img
            src={staticFile("cut_1.jpg")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.68) contrast(1.25)",
              transform: `scale(${interpolate(frame - 560, [0, 160], [1.0, 1.15], {
                easing: theme.ease.inOut,
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })})`,
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* CUT 6 (Frames 720 - 960): OUTRO FINAL SCENE */}
      <Sequence from={720} durationInFrames={240}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <Img
            src={staticFile("cut_2.jpg")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.40) blur(6px)",
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* LAYER 3: Graphics & Typography */}
      <BreakingBadge category="US Tech & Energy Alert" />

      {/* Scene 1 Caption */}
      <Sequence from={5} durationInFrames={135}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            paddingBottom: 80,
          }}
        >
          <Entrance delay={5}>
            <div
              style={{
                background: "rgba(10, 15, 30, 0.90)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 24,
                padding: "36px 30px",
                maxWidth: 960,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <WordReveal
                text="Big Tech is secretly buying nuclear power plants."
                delay={6}
                per={3}
                highlightWord="nuclear"
              />
            </div>
          </Entrance>
        </AbsoluteFill>
        <SourceCredit sourceName="Official Datacenter Tour / Wire" />
      </Sequence>

      {/* Scene 2 Caption */}
      <Sequence from={145} durationInFrames={135}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            paddingBottom: 80,
          }}
        >
          <Entrance delay={145}>
            <div
              style={{
                background: "rgba(10, 15, 30, 0.90)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 24,
                padding: "36px 30px",
                maxWidth: 960,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <WordReveal
                text="Why? Because AI is draining the US power grid at record speeds."
                delay={148}
                per={3}
                highlightWord="draining"
              />
            </div>
          </Entrance>
        </AbsoluteFill>
        <SourceCredit sourceName="Energy Regulatory Filing" />
      </Sequence>

      {/* Scene 3 Caption */}
      <Sequence from={285} durationInFrames={135}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            paddingBottom: 80,
          }}
        >
          <Entrance delay={285}>
            <div
              style={{
                background: "rgba(10, 15, 30, 0.90)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 24,
                padding: "36px 30px",
                maxWidth: 960,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <WordReveal
                text="One single AI query uses 10 TIMES more power than Google."
                delay={288}
                per={3}
                highlightWord="10"
              />
            </div>
          </Entrance>
        </AbsoluteFill>
        <SourceCredit sourceName="Semiconductor Research Lab" />
      </Sequence>

      {/* Scene 4 Caption */}
      <Sequence from={425} durationInFrames={135}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            paddingBottom: 80,
          }}
        >
          <Entrance delay={425}>
            <div
              style={{
                background: "rgba(10, 15, 30, 0.90)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 24,
                padding: "36px 30px",
                maxWidth: 960,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <WordReveal
                text="Microsoft and Google just inked historic multi-billion deals."
                delay={428}
                per={3}
                highlightWord="historic"
              />
            </div>
          </Entrance>
        </AbsoluteFill>
        <SourceCredit sourceName="White House Briefing / Wire" />
      </Sequence>

      {/* Scene 5 Caption */}
      <Sequence from={565} durationInFrames={155}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            paddingBottom: 80,
          }}
        >
          <Entrance delay={565}>
            <div
              style={{
                background: "rgba(10, 15, 30, 0.90)",
                border: `3px solid ${theme.colors.primary}`,
                borderRadius: 24,
                padding: "36px 30px",
                maxWidth: 960,
                boxShadow: "0 20px 50px rgba(0,0,0,0.8)",
              }}
            >
              <WordReveal
                text="By 2030, AI could consume 20% of America's total electricity."
                delay={568}
                per={3}
                highlightWord="20%"
              />
            </div>
          </Entrance>
        </AbsoluteFill>
        <SourceCredit sourceName="US Department of Energy" />
      </Sequence>

      {/* SCENE 6: OUTRO CALL TO ACTION (THE FINISHING!) */}
      <Sequence from={725} durationInFrames={235}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            paddingBottom: 50,
          }}
        >
          <OutroCTA delay={730} />
        </AbsoluteFill>
      </Sequence>

      {/* Bottom Progress Bar */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          height: 18,
          width: `${progressRatio * 100}%`,
          background: theme.colors.primary,
          boxShadow: `0 0 16px ${theme.colors.primary}`,
        }}
      />

      {/* LAYER 4: Color Grade Overlay */}
      <Grade />

      {/* LAYER 5: Grain & Vignette on Top */}
      <Vignette />
      <Grain />

      {/* Full 32-second Narration Audio */}
      <Audio src={staticFile("voice.mp3")} />
    </AbsoluteFill>
  );
};

'use client';

import { useEffect, useRef } from 'react';
import './Noise.css';

interface NoiseProps {
  patternSize?: number;
  patternScaleX?: number;
  patternScaleY?: number;
  patternRefreshInterval?: number;
  patternAlpha?: number;
}

export default function Noise({
  patternSize = 250,
  patternScaleX = 1,
  patternScaleY = 1,
  patternRefreshInterval = 2,
  patternAlpha = 15,
}: NoiseProps) {
  const grainRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = grainRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = patternSize;
    canvas.height = patternSize;

    let frame = 0;

    const update = () => {
      if (frame % patternRefreshInterval === 0) {
        const imageData = ctx.createImageData(patternSize, patternSize);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
          const value = Math.random() * 255;
          data[i] = value;
          data[i + 1] = value;
          data[i + 2] = value;
          data[i + 3] = patternAlpha;
        }

        ctx.putImageData(imageData, 0, 0);
      }

      frame++;
      requestAnimationFrame(update);
    };

    const animationId = requestAnimationFrame(update);

    return () => cancelAnimationFrame(animationId);
  }, [patternSize, patternRefreshInterval, patternAlpha]);

  return (
    <canvas
      ref={grainRef}
      className="noise-canvas"
      style={{
        transform: `scale(${patternScaleX}, ${patternScaleY})`,
      }}
    />
  );
}

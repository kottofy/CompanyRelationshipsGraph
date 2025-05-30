import React, { useEffect, useRef } from 'react';
import { Network } from 'vis-network/standalone';

export default function CompanyGraph({ graphData, setError }) {
  const networkRef = useRef(null);
  const visNetwork = useRef(null);

  useEffect(() => {
    if (!networkRef.current || !graphData) return;
    if (visNetwork.current) {
      visNetwork.current.destroy();
    }
    if (typeof Network !== 'function') {
      setError && setError('vis-network is not available. Please run: npm install vis-network');
      return;
    }
    visNetwork.current = new Network(networkRef.current, graphData, {
      nodes: {
        shape: 'circularImage',
        size: 60,
        font: { size: 18, vadjust: 50 },
        borderWidth: 2,
        shapeProperties: { useImageSize: false, interpolation: true, borderDashes: false },
      },
      edges: {
        arrows: 'to',
        font: { align: 'middle' },
        smooth: false,
      },
      layout: {
        improvedLayout: true,
      },
      physics: {
        stabilization: true,
        barnesHut: {
          centralGravity: 0.05,
          springLength: 350,
          springConstant: 0.01,
          avoidOverlap: 2,
        },
        minVelocity: 0.75,
      },
    });
    visNetwork.current.once('stabilizationIterationsDone', function () {
      visNetwork.current.setOptions({ physics: false });
    });
  }, [graphData, setError]);

  return (
    <div
      ref={networkRef}
      style={{
        flex: 1,
        minHeight: 0,
        height: '100%',
        width: '100%',
        border: '1px solid #ccc',
        background: '#fff',
        overflow: 'hidden',
        display: 'flex',
      }}
    />
  );
}

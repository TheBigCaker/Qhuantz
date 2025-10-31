
import React from 'react';

const iconProps = {
  width: "24",
  height: "24",
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: "2",
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

export const PlusIcon = () => (
  <svg {...iconProps}>
    <line x1="12" y1="5" x2="12" y2="19"></line>
    <line x1="5" y1="12" x2="19" y2="12"></line>
  </svg>
);

export const MinusIcon = () => (
  <svg {...iconProps}>
    <line x1="5" y1="12" x2="19" y2="12"></line>
  </svg>
);

export const BlankIcon = () => (
  <svg {...iconProps}>
    <rect x="5" y="5" width="14" height="14" rx="2" ry="2" fill="currentColor" stroke="none"></rect>
  </svg>
);

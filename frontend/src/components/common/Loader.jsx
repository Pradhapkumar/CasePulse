import React from 'react';
import { motion } from 'framer-motion';

const Loader = ({ size = "md", text = "Processing..." }) => {
  const sizes = {
    sm: "w-8 h-8",
    md: "w-16 h-16",
    lg: "w-24 h-24"
  };

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <div className="relative">
        {/* Outer pulse */}
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className={`${sizes[size]} rounded-full bg-primary/20 absolute inset-0`}
        />
        
        {/* Spinning ring */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "linear"
          }}
          className={`${sizes[size]} rounded-full border-t-2 border-r-2 border-primary border-b-2 border-l-2 border-b-transparent border-l-transparent`}
        />
        
        {/* Center dot */}
        <motion.div
          animate={{
            scale: [0.8, 1.1, 0.8],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="w-3 h-3 bg-primary rounded-full absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 shadow-[0_0_15px_rgba(59,130,246,0.5)]"
        />
      </div>
      
      {text && (
        <motion.p
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="text-primary font-medium text-sm tracking-widest uppercase"
        >
          {text}
        </motion.p>
      )}
    </div>
  );
};

export default Loader;

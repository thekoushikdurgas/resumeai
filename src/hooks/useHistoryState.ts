import { useState, useCallback } from 'react';

const HISTORY_LIMIT = 50;

export interface HistoryEntry<T> {
  state: T;
  timestamp: number;
}

export interface HistoryState<T> {
  history: HistoryEntry<T>[];
  present: number;
}

export const useHistoryState = <T>(initialState: T) => {
  const [state, setState] = useState<HistoryState<T>>({
    history: [{ state: initialState, timestamp: Date.now() }],
    present: 0,
  });

  const presentState = state.history[state.present].state;

  const set = useCallback((newState: T) => {
    setState(currentState => {
      // Prevent saving identical subsequent states
      if (JSON.stringify(newState) === JSON.stringify(currentState.history[currentState.present].state)) {
        return currentState;
      }
      const truncatedHistory = currentState.history.slice(0, currentState.present + 1);
      const newHistoryWithEntry = [...truncatedHistory, { state: newState, timestamp: Date.now() }];

      const newHistory = newHistoryWithEntry.length > HISTORY_LIMIT
        ? newHistoryWithEntry.slice(newHistoryWithEntry.length - HISTORY_LIMIT)
        : newHistoryWithEntry;
      
      return {
        history: newHistory,
        present: newHistory.length - 1,
      };
    });
  }, []);
  
  const reset = useCallback((newState: T) => {
    setState({
        history: [{ state: newState, timestamp: Date.now() }],
        present: 0,
    });
  }, []);

  const loadState = useCallback((loadedState: HistoryState<T>) => {
    if (loadedState && loadedState.history && typeof loadedState.present === 'number') {
      setState(loadedState);
    }
  }, []);

  const undo = useCallback(() => {
    setState(currentState => {
      if (currentState.present > 0) {
        return {
          ...currentState,
          present: currentState.present - 1,
        };
      }
      return currentState;
    });
  }, []);

  const redo = useCallback(() => {
    setState(currentState => {
      if (currentState.present < currentState.history.length - 1) {
        return {
          ...currentState,
          present: currentState.present + 1,
        };
      }
      return currentState;
    });
  }, []);

  const canUndo = state.present > 0;
  const canRedo = state.present < state.history.length - 1;

  return {
    state: presentState,
    setState: set,
    resetState: reset,
    loadState,
    undo,
    redo,
    canUndo,
    canRedo,
    history: state.history,
    present: state.present,
  };
};

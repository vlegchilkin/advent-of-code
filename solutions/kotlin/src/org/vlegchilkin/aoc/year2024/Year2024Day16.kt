package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*
import java.util.*
import kotlin.collections.ArrayDeque

data class State(val pos: C, val direction: Direction)

/**
 * 2024/16: Reindeer Maze
 */
class Year2024Day16(input: String) : Solution {
  private val map = input.toCSpace { it.takeIf { it != '.' } }

  override fun partAB(): Pair<Int, Int> {
    val start = map.firstNotNullOf { (pos, c) -> pos.takeIf { c == 'S' } }
    val finish = map.firstNotNullOf { (pos, c) -> pos.takeIf { c == 'E' } }
    val initStates: List<State> = listOf(State(start, Direction.E))
    val finishStates = Direction.borders().map { State(finish, it) }

    val minCosts = initStates.associateWith { 0 }.toMutableMap()
    val prioQueue = PriorityQueue<Pair<Int, State>>(compareBy { it.first })
    val backtrack = mutableMapOf<State, MutableList<State>>()

    prioQueue.addAll(minCosts.map { (k, v) -> v to k })
    while (prioQueue.isNotEmpty()) {
      val (costs, state) = prioQueue.poll()
      if (minCosts[state] != costs) continue
      if (finishStates.any { fst -> minCosts[fst]?.let { it < costs } == true }) continue

      val (pos, direction) = state
      val newStateCosts = listOf(
        State(pos + direction, direction) to costs + 1,
        State(pos, direction.turn(Side.L)) to costs + 1000,
        State(pos, direction.turn(Side.R)) to costs + 1000,
      ).filter { (np) -> map[np.pos] != '#' }

      for ((newState, newCosts) in newStateCosts) {
        val prevCosts = minCosts[newState]
        if (prevCosts == null || prevCosts > newCosts) {
          minCosts[newState] = newCosts
          prioQueue.offer(newCosts to newState)
          backtrack[newState] = mutableListOf(state)
        }
        else if (prevCosts == newCosts) {
          backtrack[newState]?.add(state)
        }
      }
    }

    val bestPathTiles = mutableSetOf<C>()
    val backTrackQueue = ArrayDeque(finishStates.filter { it in backtrack })
    while (backTrackQueue.isNotEmpty()) {
      val state = backTrackQueue.removeFirst()
      bestPathTiles.add(state.pos)
      backtrack[state]?.let { backTrackQueue.addAll(it) }
    }

    val partA = finishStates.firstNotNullOf { minCosts[it] }
    val partB = bestPathTiles.size
    return partA to partB
  }


  companion object : Test(2024, 16, { Year2024Day16(it) })
}

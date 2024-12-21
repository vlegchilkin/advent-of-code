package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*
import kotlin.collections.ArrayDeque


/**
 * 2024/16: Reindeer Maze
 */
class Year2024Day16(input: String) : Solution {
  private val map = input.toCSpace()

  override fun partAB(): Pair<Int, Int> {
    val start = map.firstNotNullOf { (pos, c) -> pos.takeIf { c == 'S' } }
    val finish = map.firstNotNullOf { (pos, c) -> pos.takeIf { c == 'E' } }
    val startVectors: List<CVector> = listOf(CVector(start, Direction.E))

    val (minCosts, finishVectors, backtrack) = findCPaths(startVectors, listOf(finish)) { costs, (pos, direction) ->
      listOf(
        CVector(pos + direction, direction) to costs + 1,
        CVector(pos, direction.turn(Side.L)) to costs + 1000,
        CVector(pos, direction.turn(Side.R)) to costs + 1000,
      ).filter { (np) -> map[np.pos] != '#' }
    }

    val bestPathTiles = mutableSetOf<C>()
    val backTrackQueue = ArrayDeque(finishVectors)
    while (backTrackQueue.isNotEmpty()) {
      val state = backTrackQueue.removeFirst()
      bestPathTiles.add(state.pos)
      backtrack[state]?.let { backTrackQueue.addAll(it.backtrack) }
    }

    val partB = bestPathTiles.size
    return minCosts to partB
  }


  companion object : Test(2024, 16, { Year2024Day16(it) })
}

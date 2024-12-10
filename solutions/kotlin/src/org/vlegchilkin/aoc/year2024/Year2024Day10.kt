package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

const val START: Int = 0
const val FINISH: Int = 9

/**
 * 2024/10: Hoof It
 */
class Year2024Day10(input: String) : Solution {
  private val map = input.toCSpace { it.digitToInt() }

  override fun partAB(): Pair<Int, Int> {
    val routesCounter = map.transform { pos, height -> if (height == START) mutableSetOf(pos) else mutableSetOf() }
    val pathsCounter = map.transform { _, high -> if (high == START) 1 else 0 }

    val heightPositions = map.entries.groupBy({ it.value }, { it.key }).toSortedMap()
    val heightPositionsStepUpSeq = heightPositions.entries.asSequence().dropWhile { (h) -> h <= START }.takeWhile { (h) -> h <= FINISH }

    heightPositionsStepUpSeq.forEach { (height, positions) ->
      for (pos in positions) {
        val stepDownNeighbours = map.links(pos, Direction.borders()) { map[it] == height - 1 }
        routesCounter[pos]?.let { posRoutes ->
          stepDownNeighbours.mapNotNull { routesCounter[it] }.forEach { lowerRoutes -> posRoutes.addAll(lowerRoutes) }
        }
        pathsCounter[pos] = stepDownNeighbours.mapNotNull { pathsCounter[it] }.sum()
      }
    }

    val finishPositions = heightPositions[FINISH] ?: emptyList()
    val differentRoutes = finishPositions.mapNotNull { routesCounter[it] }.sumOf { it.size }
    val differentPaths = finishPositions.mapNotNull { pathsCounter[it] }.sum()
    return differentRoutes to differentPaths
  }

  companion object : Test(2024, 10, { Year2024Day10(it) })
}

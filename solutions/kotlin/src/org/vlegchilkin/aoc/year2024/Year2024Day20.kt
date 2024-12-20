package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/20: Race Condition
 */
class Year2024Day20(input: String) : Solution {
  private val map = input.toCSpace { it.takeIf { it != '.' } }

  override fun partAB(): Pair<Int, Int> {
    val start = map.firstNotNullOf { (pos, c) -> pos.takeIf { c == 'S' } }
    val maze = map.transform { _, c -> if (c != '#') 'X' else null }
    val distanceFromStart = maze.findMinPaths(listOf(start)) { it in maze }
    val track = distanceFromStart.entries.sortedBy { it.value }

    fun findNumOfWaysToCheat(cheatsLimit: Int): Int {
      var counter = 0
      for (sIdx in 0 until track.size - 1) {
        val (sPos, sSteps) = track[sIdx]
        for (eIdx in sIdx + 1 until track.size) {
          val (ePos, eSteps) = track[eIdx]
          val cheatSteps = sPos.manhattanTo(ePos)
          if (cheatSteps > cheatsLimit) continue
          if (sSteps - eSteps + cheatSteps <= -100) counter++
        }
      }
      return counter
    }

    return findNumOfWaysToCheat(2) to findNumOfWaysToCheat(20)
  }

  companion object : Test(2024, 20, { Year2024Day20(it) })
}

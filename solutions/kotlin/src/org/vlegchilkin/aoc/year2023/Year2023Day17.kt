package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.Direction.*

/**
 * 2023/17: Clumsy Crucible
 */
class Year2023Day17(input: String) : Solution {
  private val space = input.toCSpace { it - '0' }

  private fun findMinPath(minSteps: Int = 1, maxSteps: Int): Int {
    val start = 0 to 0
    val finish = space.rows.last to space.cols.last
    val initStates = listOf(CVector(start, E), CVector(start, S))

    val (totalCosts) = findCPaths(initStates, listOf(finish)) { path, (pos, direction) ->
      val sides = listOf(direction.turn(Side.L), direction.turn(Side.R))
      var (newPath, newPos) = path to pos
      val result = mutableListOf<Pair<CVector, Int>>()
      for (steps in 1..maxSteps) {
        newPos += direction
        if (newPos !in space) break
        newPath += space[newPos]!!
        if (steps >= minSteps) {
          result.addAll(sides.map { sideDirection -> CVector(newPos, sideDirection) to newPath })
        }
      }
      result
    }

    return totalCosts
  }

  override fun partA(): Any {
    return findMinPath(maxSteps = 3)
  }

  override fun partB(): Any {
    return findMinPath(minSteps = 4, maxSteps = 10)
  }

  companion object : Test(2023, 17, { Year2023Day17(it) })
}

package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.Direction.*
import java.util.*

typealias State = Pair<C, Direction>

/**
 * 2023/17: Clumsy Crucible
 */
class Year2023Day17(input: String) : Solution {
  private val space = input.toCSpace { it - '0' }

  private fun findMinPath(minSteps: Int = 1, maxSteps: Int): Int {
    val start = 0 to 0
    val finish = space.rows.last to space.cols.last
    val initStates = listOf(start to E, start to S)
    val minPath = initStates.associateWith { 0 }.toMutableMap()
    val queue = PriorityQueue<Pair<Int, State>>(compareBy { it.first })

    queue.addAll(minPath.map { (k, v) -> v to k })
    while (queue.isNotEmpty()) {
      val (path, state) = queue.poll()
      if (minPath[state] != path) continue
      val (pos, direction) = state
      if (pos == finish) return path

      val sides = listOf(direction.turn(Side.L), direction.turn(Side.R))
      var (newPath, newPos) = path to pos
      for (steps in 1..maxSteps) {
        newPos += direction
        if (newPos !in space) break
        newPath += space[newPos]!!
        if (steps < minSteps) continue

        sides.forEach { newDirection ->
          val newState = newPos to newDirection
          if (minPath[newState]?.let { it <= newPath } != true) {
            minPath[newState] = newPath
            queue.offer(newPath to newState)
          }
        }
      }
    }
    throw IllegalArgumentException()
  }

  override fun partA(): Any {
    return findMinPath(maxSteps = 3)
  }

  override fun partB(): Any {
    return findMinPath(minSteps = 4, maxSteps = 10)
  }

  companion object : Test(2023, 17, { Year2023Day17(it) })
}

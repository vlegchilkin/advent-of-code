package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/18: RAM Run
 */
class Year2024Day18(input: String) : Solution {
  private val lines = input.toList { it.toIntList().toPair() }
  private val n = 70
  private val start = 0 to 0
  private val finish = n to n

  private fun findMinPath(firstLines: Int): Int? {
    val stepsData = lines.take(firstLines).map { (x, y) -> y to x }.associateWith { '#' }.toMutableMap()
    val space = CSpace(0..n, 0..n, stepsData)
    val distances = space.findMinPaths(listOf(start))
    return distances[finish]
  }

  override fun partA(): Int {
    val minPath = findMinPath(1024)
                  ?: error("there is no path to finish")
    return minPath
  }

  override fun partB(): Any {
    var (lo, hi) = 0 to lines.size
    while (lo < hi) {
      val mid = (lo + hi + 1) / 2
      if (findMinPath(mid) != null) lo = mid else hi = mid - 1
    }
    val blockerIndex = lo.takeIf { it in lines.indices }
                       ?: error("There is no blocker in any steps")
    val blocker = lines[blockerIndex]
    return "${blocker.first},${blocker.second}"
  }

  companion object : Test(2024, 18, { Year2024Day18(it) })
}

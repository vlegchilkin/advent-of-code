package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import kotlin.math.roundToLong


/**
 * 2023/21: Step Counter
 */
class Year2023Day21(input: String) : Solution {
  private val space = input.toCSpace { it.takeIf { it != '.' } }
  private val start = space.firstNotNullOf { (pos, v) -> pos.takeIf { v == 'S' } }

  init {
    space.remove(start)
  }

  override fun partAB(): Pair<Any, Any> {
    var partA: Int? = null
    var current: MutableSet<C> = mutableSetOf(start)
    val (partASteps, partBSteps) = 64 to 26501365
    val modStepValues = mutableListOf<Int>()
    val requiredMod = partBSteps.mod(space.rowsCount)

    for (step in 1..partBSteps) {
      val next = mutableSetOf<C>()
      for (pos in current) {
        val links = space.links(pos, Direction.borders()) {
          (it.first.mod(space.rowsCount) to it.second.mod(space.colsCount)) !in space
        }
        next.addAll(links)
      }
      current = next

      if (step == partASteps) partA = current.size
      if (step.mod(space.rowsCount) == requiredMod) {
        modStepValues.add(current.size)
        if (modStepValues.size == 3) break
      }
    }

    val f = modStepValues.polyfit(2).map { it.roundToLong() }
    val x = (partBSteps - requiredMod) / space.rowsCount
    val partB = f[2] * x * x + f[1] * x + f[0]

    return partA!! to partB
  }

  companion object : Test(2023, 21, { Year2023Day21(it) })
}

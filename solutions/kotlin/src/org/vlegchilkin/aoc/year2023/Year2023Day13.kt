package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/13: Point of Incidence
 */
class Year2023Day13(input: String) : Solution {
  private val spaces = input.toList("\n\n") { it.toCSpace() }

  override fun partAB(): Pair<Int, Int> {
    fun reflections(space: CSpace<Char>): Set<Int> {
      val result = mutableSetOf<Int>()

      result += (1..space.rows.last).filter { row ->
        (0..minOf(row - 1, space.rows.last - row)).all { d ->
          space.cols.all { col -> space[row - d - 1 to col] == space[row + d to col] }
        }
      }.map { it * 100 }

      result += (1..space.cols.last).filter { col ->
        (0..minOf(col - 1, space.cols.last - col)).all { d ->
          space.rows.all { row -> space[row to col - d - 1] == space[row to col + d] }
        }
      }
      return result
    }

    val baseReflections = spaces.map { reflections(it) }
    val partA = baseReflections.sumOf { it.sum() }

    val newReflections = spaces.zip(baseReflections).map { (space, baseReflection) ->
      val result = mutableSetOf<Int>()
      for ((pos, value) in space.view()) {
        if (value != null) space.remove(pos) else space[pos] = '#'
        result += reflections(space) - baseReflection
        if (value == null) space.remove(pos) else space[pos] = '#'
      }
      result
    }
    val partB = newReflections.sumOf { it.sum() }

    return partA to partB
  }

  companion object : Test(2023, 13, { Year2023Day13(it) })
}

package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*


/**
 * 2025/4: Printing Department
 */
class Year2025Day4(input: String) : Solution {
  private val space = input.toCSpace(filter = { true }, mapper = { if (it == '@') 1 else 0 })

  private fun step(space: CSpace<Int>): CSpace<Int> {
    val neighbours: CSpace<Int> = space.transform { pos, _ ->
      space.links(pos, hasPath = { space[it] == 1 }).count()
    }
    val nextSpace = space.transform { pos, _ -> if (space[pos] == 0 || neighbours[pos]!! < 4) 0 else 1 }
    return nextSpace
  }


  override fun partA(): Any {
    return space.values.sum() - step(space).values.sum()
  }

  override fun partB(): Any {
    var space = this.space
    var n = space.values.sum()
    var removed = 0
    var counter = 0

    do {
      space = step(space)
      n = space.values.sum().also {
        removed = n - it
        counter += removed
      }
    }
    while (removed > 0)

    return counter
  }

  companion object : Test(2025, 4, { Year2025Day4(it) })
}

package org.vlegchilkin.aoc

import org.junit.jupiter.api.Test
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.io.path.*
import kotlin.test.assertEquals

interface Solution {
  fun partA(): Any = ""
  fun partB(): Any = ""
  fun partAB(): Pair<Any, Any> = partA() to partB()
}

abstract class Test(private val year: Int, private val day: Int, val solution: (input: String) -> Solution) {
  companion object {
    val ROOT_PATH: Path = Paths.get("../../resources").toAbsolutePath()
  }

  @Test
  fun test() {
    for ((input, output) in getTestCases()) {
      val (a, b) = solution(input).partAB()
      assertEquals(output, a.toString() + "\n" + b.toString() + "\n")
    }
  }

  @OptIn(ExperimentalPathApi::class)
  fun getTestCases(): Sequence<Pair<String, String>> {
    val dayPath = ROOT_PATH / "$year" / "day" / "$day"
    return dayPath.walk().filter { it.extension == "out" }.sorted().map {
      val input = it.parent / "${it.fileName.name.removeSuffix("out")}in"
      Files.readString(input, Charsets.UTF_8) to Files.readString(it, Charsets.UTF_8)
    }
  }
}
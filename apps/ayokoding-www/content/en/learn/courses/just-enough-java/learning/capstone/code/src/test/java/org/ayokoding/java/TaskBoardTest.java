package org.ayokoding.java;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.Test;

final class TaskBoardTest {
    @Test
    void reportsOnlySortedOpenTasks() {
        var tasks = List.of(
                new TaskBoard.Task("zebra", new TaskBoard.Open()),
                new TaskBoard.Task("alpha", new TaskBoard.Open()),
                new TaskBoard.Task("done", new TaskBoard.Done()));

        assertEquals(List.of("alpha", "zebra"), TaskBoard.openTaskNames(tasks));
    }

    @Test
    void rendersEverySealedState() {
        assertEquals("write: open", TaskBoard.render(new TaskBoard.Task("write", new TaskBoard.Open())));
        assertEquals("review: done", TaskBoard.render(new TaskBoard.Task("review", new TaskBoard.Done())));
    }

    @Test
    void rejectsBlankTaskNames() {
        assertThrows(IllegalArgumentException.class, () -> new TaskBoard.Task(" ", new TaskBoard.Open()));
    }
}

